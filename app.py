import os
import joblib
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'neurogait_secret_key_2024_change_in_production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Initialize Login Manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    predictions = db.relationship('Prediction', backref='user', lazy=True)

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    predicted_disease = db.Column(db.String(50), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Load AI Model
model = None
scaler = None
le = None
features_list = None

def load_model():
    global model, scaler, le, features_list
    try:
        model_path = os.path.join(os.path.dirname(__file__), 'model', 'model.pkl')
        scaler_path = os.path.join(os.path.dirname(__file__), 'model', 'scaler.pkl')
        le_path = os.path.join(os.path.dirname(__file__), 'model', 'label_encoder.pkl')
        feat_path = os.path.join(os.path.dirname(__file__), 'model', 'features.pkl')
        
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        le = joblib.load(le_path)
        features_list = joblib.load(feat_path)
        print("✅ AI Model loaded successfully!")
        return True
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        import traceback
        traceback.print_exc()
        return False

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/abstract')
def abstract():
    return render_template('abstract.html')

@app.route('/charts')
def charts():
    return render_template('charts.html')

@app.route('/performance')
def performance():
    return render_template('performance.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('predict'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            return redirect(next_page if next_page else url_for('predict'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('predict'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required', 'danger')
            return redirect(url_for('signup'))
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('signup'))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters', 'danger')
            return redirect(url_for('signup'))
        
        # Check if user exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('signup'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('signup'))
        
        # Create new user
        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_pw)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Error creating account. Please try again.', 'danger')
    
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))

@app.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    if features_list is None:
        flash('Model not loaded. Please contact administrator.', 'danger')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        try:
            # Get data from form
            data = {}
            for feat in features_list:
                val = request.form.get(feat)
                data[feat] = float(val) if val else 0.0
            
            df = pd.DataFrame([data])
            df = df[features_list]
            
            # Scale and Predict
            X_scaled = scaler.transform(df)
            pred_encoded = model.predict(X_scaled)[0]
            proba = model.predict_proba(X_scaled)[0]
            
            # Decode result
            pred_class = le.inverse_transform([pred_encoded])[0]
            confidence = max(proba) * 100
            
            # Save prediction to database
            prediction = Prediction(
                user_id=current_user.id,
                predicted_disease=pred_class,
                confidence=confidence
            )
            db.session.add(prediction)
            db.session.commit()
            # Store in session
            session['result'] = pred_class
            session['confidence'] = f"{confidence:.2f}%"
            
            # Get all probabilities
            prob_dict = {cls: f"{p*100:.2f}%" for cls, p in zip(le.classes_, proba)}
            session['probabilities'] = prob_dict
            
            return redirect(url_for('result'))
            
        except Exception as e:
            error_msg = str(e)
            flash(f"Error processing data: {error_msg}", 'danger')
            return redirect(url_for('predict'))
    
    return render_template('predict.html', features=features_list)

@app.route('/result')
@login_required
def result():
    result = session.get('result', 'N/A')
    confidence = session.get('confidence', 'N/A')
    probabilities = session.get('probabilities', {})
    if result == "ALS":
        result= "Amyotrophic Lateral Sclerosis"
    elif result == "PD":
        result = "Parkinson's disorder"
    elif result == "HD":
        result = "Huntington's disorder"
    elif result == "CO":
        result = "Healthy Control"
    return render_template('result.html', result=result, confidence=confidence, probabilities=probabilities)

@app.route('/history')
@login_required
def history():
    predictions = Prediction.query.filter_by(user_id=current_user.id).order_by(Prediction.timestamp.desc()).all()
    return render_template('history.html', predictions=predictions)

# Create database and run app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create test user if not exists
        if not User.query.filter_by(username='admin').first():
            test_user = User(
                username='admin',
                email='admin@neurogait.com',
                password=generate_password_hash('admin123', method='pbkdf2:sha256')
            )
            db.session.add(test_user)
            db.session.commit()
            print("✅ Test user created: admin / admin123")
        
        # Load the AI model
        load_model()
    
    app.run(debug=True)