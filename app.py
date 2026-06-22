import os
import re
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from database import init_db, get_db, Patient

app = Flask(__name__, static_folder="static", template_folder="templates")

# Setup email regex pattern
EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

def is_valid_email(email):
    """Checks if email matches a standard format."""
    return re.match(EMAIL_REGEX, email) is not None

def is_valid_dob(dob_str):
    """Verifies that Date of Birth is in the past or present and matches YYYY-MM-DD."""
    try:
        dob_date = datetime.strptime(dob_str, "%Y-%m-%d").date()
        return dob_date <= datetime.now().date()
    except (ValueError, TypeError):
        return False

def is_positive_number(val):
    """Verifies that value can be cast to a float and is non-negative."""
    try:
        f_val = float(val)
        return f_val >= 0
    except (ValueError, TypeError):
        return False

@app.route("/")
def index():
    """Renders the main dashboard page."""
    return render_template("index.html")

@app.route("/api/patients", methods=["GET"])
def get_patients():
    """API endpoint to retrieve all patient records."""
    with get_db() as db:
        patients = db.query(Patient).order_by(Patient.created_at.desc()).all()
        return jsonify([p.to_dict() for p in patients])

@app.route("/api/patients/<int:patient_id>", methods=["GET"])
def get_patient(patient_id):
    """API endpoint to retrieve a single patient record."""
    with get_db() as db:
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if not patient:
            return jsonify({"error": "Patient record not found."}), 404
        return jsonify(patient.to_dict())

@app.route("/api/patients", methods=["POST"])
def create_patient():
    """API endpoint to create a new patient record with AI predictions."""
    data = request.json or {}
    
    # 1. Extraction and cleanup
    full_name = data.get("full_name", "").strip()
    email = data.get("email", "").strip()
    dob = data.get("dob", "").strip()
    glucose = data.get("glucose")
    haemoglobin = data.get("haemoglobin")
    cholesterol = data.get("cholesterol")
    
    # 2. Server-side validations
    if not full_name:
        return jsonify({"error": "Full Name is required."}), 400
    if not email or not is_valid_email(email):
        return jsonify({"error": "Please provide a valid email address."}), 400
    if not dob or not is_valid_dob(dob):
        return jsonify({"error": "Date of Birth must be in the past or present (YYYY-MM-DD)."}), 400
    if glucose is None or not is_positive_number(glucose):
        return jsonify({"error": "Glucose must be a positive numeric value."}), 400
    if haemoglobin is None or not is_positive_number(haemoglobin):
        return jsonify({"error": "Haemoglobin must be a positive numeric value."}), 400
    if cholesterol is None or not is_positive_number(cholesterol):
        return jsonify({"error": "Cholesterol must be a positive numeric value."}), 400
        
    g_val = float(glucose)
    h_val = float(haemoglobin)
    c_val = float(cholesterol)
    
    # 3. Trigger hybrid AI/ML prediction engine
    from prediction import predict_health_condition
    remarks = predict_health_condition(full_name, dob, g_val, h_val, c_val)
    
    # 4. Save record to DB
    with get_db() as db:
        patient = Patient(
            full_name=full_name,
            email=email,
            dob=dob,
            glucose=g_val,
            haemoglobin=h_val,
            cholesterol=c_val,
            remarks=remarks
        )
        db.add(patient)
        db.commit()
        db.refresh(patient)
        return jsonify(patient.to_dict()), 201

@app.route("/api/patients/<int:patient_id>", methods=["PUT"])
def update_patient(patient_id):
    """API endpoint to update an existing patient record."""
    data = request.json or {}
    
    # 1. Extraction and cleanup
    full_name = data.get("full_name", "").strip()
    email = data.get("email", "").strip()
    dob = data.get("dob", "").strip()
    glucose = data.get("glucose")
    haemoglobin = data.get("haemoglobin")
    cholesterol = data.get("cholesterol")
    
    # 2. Server-side validations
    if not full_name:
        return jsonify({"error": "Full Name is required."}), 400
    if not email or not is_valid_email(email):
        return jsonify({"error": "Please provide a valid email address."}), 400
    if not dob or not is_valid_dob(dob):
        return jsonify({"error": "Date of Birth must be in the past or present (YYYY-MM-DD)."}), 400
    if glucose is None or not is_positive_number(glucose):
        return jsonify({"error": "Glucose must be a positive numeric value."}), 400
    if haemoglobin is None or not is_positive_number(haemoglobin):
        return jsonify({"error": "Haemoglobin must be a positive numeric value."}), 400
    if cholesterol is None or not is_positive_number(cholesterol):
        return jsonify({"error": "Cholesterol must be a positive numeric value."}), 400
        
    g_val = float(glucose)
    h_val = float(haemoglobin)
    c_val = float(cholesterol)
    
    with get_db() as db:
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if not patient:
            return jsonify({"error": "Patient record not found."}), 404
            
        # Re-run AI predictions only if inputs affecting the assessment have changed
        inputs_changed = (
            patient.glucose != g_val or 
            patient.haemoglobin != h_val or 
            patient.cholesterol != c_val or
            patient.full_name != full_name or
            patient.dob != dob
        )
        
        patient.full_name = full_name
        patient.email = email
        patient.dob = dob
        patient.glucose = g_val
        patient.haemoglobin = h_val
        patient.cholesterol = c_val
        
        if inputs_changed:
            from prediction import predict_health_condition
            patient.remarks = predict_health_condition(full_name, dob, g_val, h_val, c_val)
            
        db.commit()
        db.refresh(patient)
        return jsonify(patient.to_dict())

@app.route("/api/patients/<int:patient_id>", methods=["DELETE"])
def delete_patient(patient_id):
    """API endpoint to delete a patient record."""
    with get_db() as db:
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if not patient:
            return jsonify({"error": "Patient record not found."}), 404
        db.delete(patient)
        db.commit()
        return jsonify({"message": "Patient record deleted successfully."})

# Initialize the Database Tables & start Flask
if __name__ == "__main__":
    print("Initializing Database tables...")
    init_db()
    print("Starting Flask web server on http://localhost:5000...")
    app.run(host="0.0.0.0", port=5000, debug=True)
