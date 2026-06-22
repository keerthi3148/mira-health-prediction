import os
import unittest
import json
from datetime import datetime, timedelta

# Redirect database configurations to an isolated test database
import database
database.DATABASE_URL = "sqlite:///test_patients.db"

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
database.engine = create_engine(database.DATABASE_URL, connect_args={"check_same_thread": False})
database.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=database.engine)

from app import app, init_db

class MiraBackendTestCase(unittest.TestCase):
    """
    Test suite verifying CRUD operations, data validations, 
    and error handling in the MIRA Flask backend.
    """
    
    def setUp(self):
        """Initializes database tables and configures Flask test client."""
        app.config["TESTING"] = True
        self.client = app.test_client()
        
        # Initialize the fresh test database tables
        init_db()
        
    def tearDown(self):
        """Cleans up the database session and drops all test tables."""
        database.Base.metadata.drop_all(bind=database.engine)
        # Safely remove the test database file if it exists
        if os.path.exists("test_patients.db"):
            try:
                os.remove("test_patients.db")
            except OSError:
                pass

    def test_create_patient_success(self):
        """Verifies creating a patient with valid inputs generates remarks and returns 201."""
        payload = {
            "full_name": "Alexander Fleming",
            "email": "alex.fleming@penicillin.org",
            "dob": "1881-08-06",
            "glucose": 90.5,
            "haemoglobin": 15.1,
            "cholesterol": 180.0
        }
        response = self.client.post("/api/patients", 
                                    data=json.dumps(payload),
                                    content_type="application/json")
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["full_name"], "Alexander Fleming")
        self.assertEqual(data["email"], "alex.fleming@penicillin.org")
        self.assertEqual(data["glucose"], 90.5)
        self.assertTrue("remarks" in data)
        self.assertIsNotNone(data["remarks"])
        self.assertIn("ML Classification", data["remarks"])

    def test_create_patient_invalid_email(self):
        """Verifies server-side validation rejects invalid email structures."""
        payload = {
            "full_name": "Edward Jenner",
            "email": "edward.jenner@vaccine", # Missing TLD
            "dob": "1749-05-17",
            "glucose": 95.0,
            "haemoglobin": 14.5,
            "cholesterol": 190.0
        }
        response = self.client.post("/api/patients", 
                                    data=json.dumps(payload),
                                    content_type="application/json")
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Please provide a valid email address.")

    def test_create_patient_future_dob(self):
        """Verifies server-side validation rejects future dates of birth."""
        future_date = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")
        payload = {
            "full_name": "Future Patient",
            "email": "future@domain.com",
            "dob": future_date,
            "glucose": 95.0,
            "haemoglobin": 14.5,
            "cholesterol": 190.0
        }
        response = self.client.post("/api/patients", 
                                    data=json.dumps(payload),
                                    content_type="application/json")
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Date of Birth must be in the past or present (YYYY-MM-DD).")

    def test_create_patient_negative_metrics(self):
        """Verifies server-side validation rejects negative biomarker metrics."""
        payload = {
            "full_name": "Marie Curie",
            "email": "marie.curie@sorbonne.fr",
            "dob": "1867-11-07",
            "glucose": -10.0, # Negative value
            "haemoglobin": 12.0,
            "cholesterol": 190.0
        }
        response = self.client.post("/api/patients", 
                                    data=json.dumps(payload),
                                    content_type="application/json")
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Glucose must be a positive numeric value.")

    def test_read_patients(self):
        """Verifies fetching patient list yields all records."""
        # Pre-populate database
        payload = {
            "full_name": "Louis Pasteur",
            "email": "louis@pasteur.fr",
            "dob": "1822-12-27",
            "glucose": 85.0,
            "haemoglobin": 13.8,
            "cholesterol": 210.0
        }
        self.client.post("/api/patients", 
                         data=json.dumps(payload),
                         content_type="application/json")
                         
        response = self.client.get("/api/patients")
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["full_name"], "Louis Pasteur")

    def test_update_patient(self):
        """Verifies updating details modifications persist and refresh predictions."""
        # Create record
        payload = {
            "full_name": "Robert Koch",
            "email": "robert@koch.de",
            "dob": "1843-12-11",
            "glucose": 80.0,
            "haemoglobin": 14.0,
            "cholesterol": 180.0
        }
        create_res = self.client.post("/api/patients", 
                                     data=json.dumps(payload),
                                     content_type="application/json")
        patient_id = json.loads(create_res.data)["id"]
        
        # Update details (metabolic changes)
        update_payload = {
            "full_name": "Robert Koch",
            "email": "robert.koch@charite.de",
            "dob": "1843-12-11",
            "glucose": 150.0, # High glucose now
            "haemoglobin": 14.0,
            "cholesterol": 180.0
        }
        
        update_res = self.client.put(f"/api/patients/{patient_id}",
                                    data=json.dumps(update_payload),
                                    content_type="application/json")
        data = json.loads(update_res.data)
        
        self.assertEqual(update_res.status_code, 200)
        self.assertEqual(data["email"], "robert.koch@charite.de")
        self.assertEqual(data["glucose"], 150.0)
        # Check that classification shifted to Glucose Risk
        self.assertIn("Glucose / Metabolic Risk Alert", data["remarks"])

    def test_delete_patient(self):
        """Verifies deleting a patient removes them from the database."""
        # Create record
        payload = {
            "full_name": "Jonas Salk",
            "email": "jonas.salk@pitt.edu",
            "dob": "1914-10-28",
            "glucose": 92.0,
            "haemoglobin": 15.0,
            "cholesterol": 170.0
        }
        create_res = self.client.post("/api/patients", 
                                     data=json.dumps(payload),
                                     content_type="application/json")
        patient_id = json.loads(create_res.data)["id"]
        
        # Delete record
        delete_res = self.client.delete(f"/api/patients/{patient_id}")
        self.assertEqual(delete_res.status_code, 200)
        
        # Verify removal
        get_res = self.client.get(f"/api/patients/{patient_id}")
        self.assertEqual(get_res.status_code, 404)

if __name__ == "__main__":
    unittest.main()
