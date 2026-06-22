import os
import pickle
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Clinical Ranges & Info
CLINICAL_GUIDELINES = {
    "glucose": {
        "normal": "Normal blood glucose (< 100 mg/dL).",
        "hypo": "Low blood glucose / Hypoglycemia (< 70 mg/dL). May cause dizziness and fatigue. Eat fast-acting carbs.",
        "prediabetes": "Prediabetes range (100-125 mg/dL). Elevated risk of developing Type 2 Diabetes. Recommend diet adjustments.",
        "diabetes": "High blood glucose / Diabetes range (>= 126 mg/dL). Consult a physician for an HbA1c screening test."
    },
    "haemoglobin": {
        "normal": "Normal haemoglobin levels (12.0 - 17.5 g/dL).",
        "low": "Low haemoglobin / Anemic range (< 12.0 g/dL). Can cause fatigue. Recommend iron-rich diet or supplements.",
        "high": "High haemoglobin level (> 17.5 g/dL). Monitor hydration and check with a doctor if persistent."
    },
    "cholesterol": {
        "normal": "Normal cholesterol levels (< 200 mg/dL). Low cardiovascular risk.",
        "borderline": "Borderline high cholesterol (200-239 mg/dL). Monitor saturated fats intake and increase fiber.",
        "high": "High cholesterol range (>= 240 mg/dL). Increased cardiovascular risk. Recommend lipid profile assessment."
    }
}

LABEL_MAPPING = {
    0: "Excellent Health / Low Risk",
    1: "Glucose / Metabolic Risk Alert",
    2: "Haemoglobin / Anemia Risk Alert",
    3: "Cardiovascular / Cholesterol Risk Alert",
    4: "Multi-Risk Alert (Multiple abnormal metrics)"
}

def load_ml_model():
    """Loads the pickled machine learning model, training it if it doesn't exist."""
    model_path = os.path.join(os.path.dirname(__file__), "health_model.pkl")
    
    if not os.path.exists(model_path):
        print("Model file not found. Auto-training classifier...")
        try:
            from train_model import train_and_save_model
            train_and_save_model()
        except Exception as e:
            print(f"Failed to auto-train model: {e}")
            return None
            
    try:
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        return model
    except Exception as e:
        print(f"Error loading model from {model_path}: {e}")
        return None

def get_local_health_remarks(glucose, haemoglobin, cholesterol, predicted_class):
    """Generates detailed, structured clinical remarks locally if Gemini API is unavailable."""
    remarks_list = []
    
    # ML Class description
    remarks_list.append(f"**ML Classification:** {LABEL_MAPPING.get(predicted_class, 'Unknown Risk')}\n")
    
    # Glucose check
    if glucose < 70:
        remarks_list.append(f"• {CLINICAL_GUIDELINES['glucose']['hypo']}")
    elif glucose < 100:
        remarks_list.append(f"• {CLINICAL_GUIDELINES['glucose']['normal']}")
    elif glucose < 126:
        remarks_list.append(f"• {CLINICAL_GUIDELINES['glucose']['prediabetes']}")
    else:
        remarks_list.append(f"• {CLINICAL_GUIDELINES['glucose']['diabetes']}")
        
    # Haemoglobin check
    if haemoglobin < 12.0:
        remarks_list.append(f"• {CLINICAL_GUIDELINES['haemoglobin']['low']}")
    elif haemoglobin <= 17.5:
        remarks_list.append(f"• {CLINICAL_GUIDELINES['haemoglobin']['normal']}")
    else:
        remarks_list.append(f"• {CLINICAL_GUIDELINES['haemoglobin']['high']}")
        
    # Cholesterol check
    if cholesterol < 200:
        remarks_list.append(f"• {CLINICAL_GUIDELINES['cholesterol']['normal']}")
    elif cholesterol < 240:
        remarks_list.append(f"• {CLINICAL_GUIDELINES['cholesterol']['borderline']}")
    else:
        remarks_list.append(f"• {CLINICAL_GUIDELINES['cholesterol']['high']}")
        
    # Add summary advice
    remarks_list.append("\n**Recommendations:**")
    if predicted_class == 0:
        remarks_list.append("Maintain your active lifestyle, balanced diet, and hydration. Schedule a routine annual checkup.")
    elif predicted_class == 1:
        remarks_list.append("Consider reducing refined carbohydrates and sugar. Engage in moderate cardiovascular exercises.")
    elif predicted_class == 2:
        remarks_list.append("Increase intake of iron-rich foods (leafy greens, beans, red meat). Monitor iron levels with a doctor.")
    elif predicted_class == 3:
        remarks_list.append("Limit trans fats and saturated fats. Incorporate omega-3 fatty acids, oats, and soluble fiber.")
    else:
        remarks_list.append("You have multiple out-of-range parameters. We strongly recommend sharing these test results with a primary healthcare provider for a customized treatment plan.")

    return "\n".join(remarks_list)

def predict_health_condition(patient_name, dob, glucose, haemoglobin, cholesterol):
    """
    Predicts patient health status.
    First runs local ML classifier, then augments with Gemini API (if available) or standard clinical templates.
    """
    # 1. Run local ML prediction
    model = load_ml_model()
    predicted_class = 0
    
    if model is not None:
        try:
            # Predict expects shape: [[glucose, haemoglobin, cholesterol]] with feature names
            import pandas as pd
            features = pd.DataFrame(
                [[glucose, haemoglobin, cholesterol]], 
                columns=["glucose", "haemoglobin", "cholesterol"]
            )
            pred = model.predict(features)
            predicted_class = int(pred[0])
        except Exception as e:
            print(f"Error during ML prediction: {e}")
            
    # 2. Call external AI/ML API (Gemini) if API key is present
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        print("GEMINI_API_KEY found. Calling external Gemini API...")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        prompt = (
            f"You are MIRA, a highly intelligent clinical diagnostic AI. "
            f"Generate a professional, warm, and highly structured medical analysis remark for a patient named {patient_name} "
            f"(DOB: {dob}) based on their blood test results:\n"
            f"- Glucose: {glucose} mg/dL\n"
            f"- Haemoglobin: {haemoglobin} g/dL\n"
            f"- Cholesterol: {cholesterol} mg/dL\n\n"
            f"Our ML model classified this patient as: '{LABEL_MAPPING.get(predicted_class)}'.\n\n"
            f"Structure your response exactly like this:\n"
            f"**ML Classification:** {LABEL_MAPPING.get(predicted_class)}\n\n"
            f"**Analysis:** [Provide a patient-friendly analysis of their metrics. Mention which values are normal/abnormal based on common ranges: Glucose <100, Haemoglobin 12-17.5, Cholesterol <200. Keep it concise, 2-3 sentences]\n\n"
            f"**Recommendations:** [Provide 2 targeted lifestyle or diet recommendations based on their results, and add a friendly disclaimer about consulting a physician. 2-3 sentences]"
        )
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "maxOutputTokens": 250,
                "temperature": 0.4
            }
        }
        
        try:
            response = requests.post(url, json=payload, timeout=8)
            if response.status_code == 200:
                data = response.json()
                ai_text = data["contents"][0]["parts"][0]["text"].strip()
                return ai_text
            else:
                print(f"Gemini API returned status code {response.status_code}: {response.text}")
        except Exception as e:
            print(f"Failed to communicate with Gemini API: {e}")
            
    # Fallback to local clinical engine
    print("Using local clinical templates for prediction remarks.")
    return get_local_health_remarks(glucose, haemoglobin, cholesterol, predicted_class)
