# MIRA | Health Intelligence Portal

Welcome to the **MIRA (Medical Intelligence Robotic Automation)** Health Prediction Application. This project represents the completed **Task 1: Evaluation of AI/ML Skills** technical assessment for the Junior AI/ML Developer role. 

This application provides a comprehensive portal for healthcare practitioners to manage patient records and instantly assess metabolic and hematologic health risks using a hybrid Artificial Intelligence and Machine Learning approach.

---

## 🚀 Key Features

1. **Full CRUD Operations**: Create, read, update, and delete patient records with a clean, reactive layout.
2. **Hybrid AI/ML Prediction Engine**:
   - **Custom ML Model**: Uses a pre-trained `scikit-learn` Random Forest Classifier to categorize patient risk factors based on blood levels.
   - **Generative AI Integration**: Dynamically calls Google's **Gemini API** using a secure key in `.env` to generate personalized, conversational medical analysis and lifestyle recommendations.
   - **Clinical Rules Fallback**: If the Gemini API key is missing or offline, the app executes a rules-based expert system utilizing official clinical ranges.
3. **Advanced Data Accuracy & Validation**: Dual-layer (client-side and server-side) validations enforcing standard email formats, past dates of birth, and positive numeric values for lab tests.
4. **Stunning Glassmorphism Interface**: A high-fidelity, responsive dark-theme dashboard utilizing premium typography (`Outfit`, `Plus Jakarta Sans`), neon glow accents, micro-animations, and visual biomarker gauges.
5. **Persistent Storage**: Utilizes an SQLite database managed with **SQLAlchemy** for structure, integrity, and clean CRUD query operations.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.10+, Flask, SQLAlchemy (ORM), SQLite (DBMS), Scikit-learn (ML), Python-Dotenv.
- **Frontend**: HTML5 (Semantic Structure), Vanilla CSS3 (Custom Glassmorphism Design System), Vanilla JS (Fetch API, DOM rendering, client-side validation).
- **Testing**: Python `unittest` framework.

---

## 📁 Repository Structure

```
assessment/
├── app.py                  # Flask web server & REST API routes
├── database.py             # SQLite connection & SQLAlchemy Patient Model
├── prediction.py           # Hybrid AI/ML Prediction Engine
├── train_model.py          # Machine learning model training script (RandomForest)
├── test_backend.py         # Automated API & validation unit tests
├── requirements.txt        # Python dependency manifest
├── .env.example            # Environment variables configuration template
├── .env                    # Local environment config (git-ignored)
├── templates/
│   └── index.html          # Main SPA dashboard HTML structure
└── static/
    ├── css/
    │   └── style.css       # Custom CSS styling (layout, themes, sliders, toasts)
    └── js/
        └── app.js          # JS controller (validation, CRUD fetch, gauges calculation)
```

---

## 📊 AI/ML Biomarker Clinical Ranges

MIRA classifies patient conditions and renders them visually in the biomarker panels using the following standardized clinical ranges:

- **Fasting Glucose**:
  - `Hypoglycemia`: < 70 mg/dL (Color: Blue)
  - `Normal`: 70 - 99 mg/dL (Color: Green)
  - `Prediabetes`: 100 - 125 mg/dL (Color: Amber)
  - `Diabetes`: >= 126 mg/dL (Color: Red)
- **Haemoglobin**:
  - `Anemic / Low`: < 12.0 g/dL (Color: Red)
  - `Normal`: 12.0 - 17.5 g/dL (Color: Green)
  - `High`: > 17.5 g/dL (Color: Amber)
- **Total Cholesterol**:
  - `Desirable / Normal`: < 200 mg/dL (Color: Green)
  - `Borderline High`: 200 - 239 mg/dL (Color: Amber)
  - `High`: >= 240 mg/dL (Color: Red)

---

## ⚙️ Installation & Setup

Follow these steps to run the application locally on your computer:

### 1. Install Dependencies
Ensure you have Python 3.10+ installed. Install the required libraries:
```bash
pip install -r requirements.txt
```
*(Note: If you already have `flask`, `sqlalchemy`, `scikit-learn`, `requests`, and `python-dotenv` installed in your environment, you can skip this step).*

### 2. Configure Environment Variables
1. Copy the `.env.example` file to a new file named `.env`:
   ```bash
   copy .env.example .env
   ```
2. Open `.env` and add your Google Gemini API key if you'd like to test the Generative AI detailed summaries:
   ```env
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   ```
   *If you do not specify a key, the application will run fully local, utilizing the trained RandomForest model and internal clinical templates to write remarks.*

### 3. Run the Application
Start the Flask server:
```bash
python app.py
```
Upon startup:
- The database schema is initialized, and `patients.db` is created.
- The system checks for the presence of the `health_model.pkl` file. If not found, it runs `train_model.py` automatically to train a new Random Forest model on 2,000 synthetic patient profiles.

### 4. Access the Dashboard
Open your browser and navigate to:
```
http://localhost:5000
```

---

## 🧪 Running Automated Tests

To execute the suite of backend unit tests (checking CRUD endpoints, validator logic, and DB states):
```bash
python -m unittest test_backend.py
```

---

## 🔒 Security Compliance

Before uploading this codebase, all API keys, sensitive tokens, databases, and cached model binaries (except the template `.pkl` for quick loading) have been decoupled.
- The `.env` file is excluded from git tracking.
- The database file `patients.db` is excluded from git tracking.
