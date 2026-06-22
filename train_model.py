import os
import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

def generate_synthetic_data(num_samples=1500, random_seed=42):
    """
    Generates synthetic patient blood test data and labels them into health classes:
    0: Healthy
    1: Diabetic/Glucose Risk (Hypoglycemia / Prediabetes / Diabetes)
    2: Anemic/Haemoglobin Risk (Low Haemoglobin)
    3: Cardiovascular/Cholesterol Risk (High Cholesterol)
    4: Multi-Risk Alert (More than one abnormal metric)
    """
    np.random.seed(random_seed)
    
    # Generate random features within common clinical ranges
    # Glucose: 50 to 220 mg/dL
    glucose = np.random.uniform(50, 220, num_samples)
    # Haemoglobin: 7 to 19 g/dL
    haemoglobin = np.random.uniform(7, 19, num_samples)
    # Cholesterol: 120 to 320 mg/dL
    cholesterol = np.random.uniform(120, 320, num_samples)
    
    data = pd.DataFrame({
        'glucose': glucose,
        'haemoglobin': haemoglobin,
        'cholesterol': cholesterol
    })
    
    labels = []
    for idx, row in data.iterrows():
        g, h, c = row['glucose'], row['haemoglobin'], row['cholesterol']
        
        # Check individual risk flags
        g_abnormal = (g < 70 or g >= 100)
        h_abnormal = (h < 12.0)
        c_abnormal = (c >= 200)
        
        abnormal_count = sum([g_abnormal, h_abnormal, c_abnormal])
        
        if abnormal_count == 0:
            labels.append(0)  # Healthy
        elif abnormal_count > 1:
            labels.append(4)  # Multi-Risk
        else:  # Exactly 1 abnormality
            if g_abnormal:
                labels.append(1)  # Glucose Risk
            elif h_abnormal:
                labels.append(2)  # Haemoglobin Risk
            else:
                labels.append(3)  # Cholesterol Risk
                
    data['label'] = labels
    return data

def train_and_save_model():
    """Trains the RandomForestClassifier model and pickles it to disk."""
    print("Generating synthetic clinical dataset...")
    df = generate_synthetic_data(num_samples=2000)
    
    X = df[['glucose', 'haemoglobin', 'cholesterol']]
    y = df['label']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    print(f"Dataset class distribution:\n{y.value_counts()}")
    print("Training Random Forest Classifier...")
    
    # Train the model
    model = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate model
    train_acc = model.score(X_train, y_train)
    test_acc = model.score(X_test, y_test)
    print(f"Model Training Accuracy: {train_acc * 100:.2f}%")
    print(f"Model Testing Accuracy: {test_acc * 100:.2f}%")
    
    model_path = os.path.join(os.path.dirname(__file__), "health_model.pkl")
    print(f"Saving model to {model_path}...")
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
        
    print("Model trained and saved successfully!")

if __name__ == "__main__":
    train_and_save_model()
