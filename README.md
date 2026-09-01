# NeuroGait AI: Early Detection of Neurodegenerative Diseases

## 📖 Project Overview

**NeuroGait AI** is a full-stack web application designed to assist in the early detection of neurodegenerative diseases (ALS, Parkinson's, Huntington's) by analyzing patient gait patterns.

The system utilizes an optimized **Stacking Ensemble Machine Learning Model** (combining Random Forest, XGBoost, and Gradient Boosting with a Logistic Regression meta-learner). By aggregating raw stride-level data into patient-level statistical features and engineering novel biomarkers (like the Severity-Speed Ratio), the model achieves a fair accuracy of **81.15%**, successfully eliminating data leakage and outperforming baseline frameworks.

## ✨ Key Features

* **Secure User Authentication:** Sign up, login, and session management using Flask-Login and SQLite.
* **Real-Time AI Prediction:** Input patient gait metrics and receive instant disease classification with confidence scores.
* **Interactive Data Visualization:** Professional charts showing dataset distribution, feature correlations, and algorithm performance (Confusion Matrix, ROC Curves).
* **Prediction History:** Logged-in users can track their past diagnostic predictions.
* **Robust ML Pipeline:** Patient-level aggregation, Standard Scaling, and 5-Fold Stratified Cross-Validation.

## 🛠️ Tech Stack

* **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-Login
* **Machine Learning:** Scikit-Learn, XGBoost, Pandas, NumPy, Joblib
* **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5, Chart.js
* **Database:** SQLite

## 🚀 How to Run and Execute the Project

Follow these step-by-step instructions to set up and run the NeuroGait AI web application on your local machine.

### Prerequisites

* **Python:** Version 3.9 or higher (Anaconda distribution is highly recommended).
* **Git:** Installed on your system.
* **IDE:** VS Code, PyCharm, or Jupyter Notebook.

### Step 1: Clone the Repository

Open your terminal or Anaconda Prompt and run the following command to download the project:

```bash
git clone https://github.com/HarshithSaiChand/NeuroGait-AI.git
cd NeuroGait-AI
```


<p align="center">
  <a href="https://github.com/HarshithSaiChand/NeuroGait-AI/raw/refs/heads/main/setup.mp4">
    <img src="https://shields.io" alt="Watch Setup Video">
  </a>
</p>


### Step 2: Create a Virtual Environment (Recommended)

It is best practice to run the project in an isolated environment to avoid dependency conflicts.

```bash
# Using Anaconda (Recommended)
conda create -n neurogait python=3.10 -y
conda activate neurogait

# OR using standard Python venv
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

Install all the required Python libraries listed in the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

*(Note: If you encounter version conflicts, ensure your `scikit-learn` version matches the one used to train the model, typically `1.2.2` or higher).*

### Step 4: Run the Web Application

Once the dependencies are installed, start the Flask server by running:

```bash
python app.py
```

You should see output in your terminal indicating the server is running, usually at `http://127.0.0.1:5000`.

### Step 5: Access the Application

Open your web browser and navigate to:

👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

**Default Login Credentials (for testing):**

* **Username:** `admin`
* **Password:** `admin123`

### Step 6: (Optional) Retrain the Model

If you wish to retrain the AI model from scratch or view the data processing pipeline:

1. Open `OPTIC.ipynb` in Jupyter Notebook or VS Code.
2. Run the cells sequentially.
3. The notebook will process the raw `.ts` files, train the Stacking Ensemble model, generate evaluation graphs, and automatically save the updated `.pkl` files into the `model/` folder.

## 📁 Project Structure

```text
NeuroGaitApp/
│
├── app.py                  # Main Flask application and routes
├── requirements.txt        # Python dependencies
├── OPTIC.ipynb             # Jupyter Notebook for model training
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
```

## ⚠️ Troubleshooting Common Issues

### 1. `AttributeError: 'LogisticRegression' object has no attribute 'multi_class'`

**Cause:** This happens if the `scikit-learn` library on the machine running the app is older than the version used to train the model.

**Fix:** Upgrade scikit-learn to the latest version:

```bash
pip install --upgrade scikit-learn
```

### 2. `FileNotFoundError: No such file or directory: 'model/model.pkl'`

**Cause:** The application cannot find the trained model files.

**Fix:** Ensure that the `model/` folder exists in the same directory as `app.py` and contains all four `.pkl` files (`model.pkl`, `scaler.pkl`, `label_encoder.pkl`, `features.pkl`).

### 3. Database Errors on First Run

**Fix:** If you encounter database locking or schema errors, simply delete the `instance/users.db` file and restart the application. It will automatically recreate the database and the default admin user.

## 📄 License

This project is created for academic and research purposes.
```

The complete `README.md` has been created at:

**`/home/workdir/artifacts/README.md`**

It includes all the sections you provided:

- Project Overview
- Key Features
- Tech Stack
- How to Run and Execute (with prerequisites and 6 detailed steps)
- Project Structure
- Troubleshooting Common Issues
- License

You can download it from the artifacts folder or copy its contents directly into your GitHub repository.