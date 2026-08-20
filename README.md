# NeuroGait AI: Early Detection of Neurodegenerative Diseases

## 📖 Project Overview
**NeuroGait AI** is a full-stack web application designed to assist in the early detection of neurodegenerative diseases (ALS, Parkinson's, Huntington's) by analyzing patient gait patterns. 

The system utilizes an optimized **Stacking Ensemble Machine Learning Model** (combining Random Forest, XGBoost, and Gradient Boosting with a Logistic Regression meta-learner). By aggregating raw stride-level data into patient-level statistical features and engineering novel biomarkers (like the Severity-Speed Ratio), the model achieves a fair accuracy of **81.15%**, successfully eliminating data leakage and outperforming baseline frameworks.

## ✨ Key Features
*   **Secure User Authentication:** Sign up, login, and session management using Flask-Login and SQLite.
*   **Real-Time AI Prediction:** Input patient gait metrics and receive instant disease classification with confidence scores.
*   **Interactive Data Visualization:** Professional charts showing dataset distribution, feature correlations, and algorithm performance (Confusion Matrix, ROC Curves).
*   **Prediction History:** Logged-in users can track their past diagnostic predictions.
*   **Robust ML Pipeline:** Patient-level aggregation, Standard Scaling, and 5-Fold Stratified Cross-Validation.

## 🛠️ Tech Stack
*   **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-Login
*   **Machine Learning:** Scikit-Learn, XGBoost, Pandas, NumPy, Joblib
*   **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5, Chart.js
*   **Database:** SQLite

## 📁 Project Structure
```text
NeuroGaitApp/
│
├── app.py                  # Main Flask application and routes
├── requirements.txt        # Python dependencies
├── generate_graphs.py      # Script to generate dataset charts
├── generate_performance_graphs.py # Script to generate ML metrics
│
├── model/                  # Trained ML models (DO NOT DELETE)
│   ├── model.pkl
│   ├── scaler.pkl
│   ├── label_encoder.pkl
│   └── features.pkl
│
├── instance/               # SQLite database (auto-generated)
│   └── users.db
│
├── static/                 # CSS, JS, and generated images
├── templates/              # HTML Jinja2 templates
└── dataset.csv             # Raw/Processed dataset