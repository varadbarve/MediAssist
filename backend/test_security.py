"""
Security Verification Script for MediAssist AI
Tests all implemented security layers using FastAPI TestClient.
"""

import sys
import os
import unittest
import io
import time
from sqlalchemy import text

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from main import app
from app.db.session import SessionLocal, engine
from app.models.patient import Patient
from app.models.user import User
from app.models.audit_log import AuditLog
from app.models.report import Report
from app.models.prescription import Prescription

class TestMediAssistSecurity(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.db = SessionLocal()
        # Clean up any existing test user
        cls.db.query(User).filter(User.email == "test_doctor@clinic.com").delete()
        cls.db.query(Patient).filter(Patient.gender == "TestMale").delete()
        cls.db.commit()

    @classmethod
    def tearDownClass(cls):
        # Clean up test data
        cls.db.query(User).filter(User.email == "test_doctor@clinic.com").delete()
        cls.db.query(Patient).filter(Patient.gender == "TestMale").delete()
        cls.db.commit()
        cls.db.close()

    def test_01_user_registration_and_login(self):
        print("\n--- Testing Layer 9: Authentication Flow ---")
        # 1. Register User
        reg_payload = {
            "email": "test_doctor@clinic.com",
            "password": "securepassword123",
            "full_name": "Dr. Test Doctor",
            "role": "doctor"
        }
        response = self.client.post("/api/v1/auth/register", json=reg_payload)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["email"], "test_doctor@clinic.com")
        self.assertEqual(data["role"], "doctor")
        self.assertTrue(data["is_active"])

        # Check password is not returned plain or hashed in UserResponse
        self.assertNotIn("password", data)
        self.assertNotIn("hashed_password", data)

        # 2. Login User
        login_payload = {
            "email": "test_doctor@clinic.com",
            "password": "securepassword123"
        }
        response = self.client.post("/api/v1/auth/login", json=login_payload)
        self.assertEqual(response.status_code, 200)
        login_data = response.json()
        self.assertIn("access_token", login_data)
        self.assertEqual(login_data["token_type"], "bearer")
        self.assertEqual(login_data["user"]["email"], "test_doctor@clinic.com")
        
        # Save token for other tests
        self.__class__.token = login_data["access_token"]
        print("Registration and Login successful. Token obtained.")

    def test_02_auth_protection(self):
        print("\n--- Testing Layer 9: Auth Protection on Endpoints ---")
        # Access protected endpoint without token
        response = self.client.get("/api/v1/auth/me")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["detail"], "Not authenticated")

        # Access with invalid token
        headers = {"Authorization": "Bearer invalid_token_here"}
        response = self.client.get("/api/v1/auth/me", headers=headers)
        self.assertEqual(response.status_code, 401)
        
        # Access with valid token
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.client.get("/api/v1/auth/me", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["email"], "test_doctor@clinic.com")
        print("Endpoint protection verified. Only valid tokens allowed.")

    def test_03_input_validation(self):
        print("\n--- Testing Layer 4: Input Validation & Sanitization ---")
        headers = {"Authorization": f"Bearer {self.token}"}

        # 1. Invalid phone number format
        pdf_file = io.BytesIO(b"%PDF-1.4\n%mock pdf content")
        data = {
            "patient_id": "PAT-12345",
            "patient_phone_number": "12345",  # Should be E.164 format
            "prescription_notes": "Take Vitamin D daily."
        }
        files = {"file": ("report.pdf", pdf_file, "application/pdf")}
        response = self.client.post("/api/v1/reports/upload", headers=headers, data=data, files=files)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid phone number", response.json()["detail"])

        # 2. Invalid patient ID format
        pdf_file = io.BytesIO(b"%PDF-1.4\n%mock pdf content")
        data = {
            "patient_id": "PATIENT_ID_WITH_SPECIAL_CHARS!@#",
            "patient_phone_number": "+919876543210",
            "prescription_notes": "Take Vitamin D daily."
        }
        files = {"file": ("report.pdf", pdf_file, "application/pdf")}
        response = self.client.post("/api/v1/reports/upload", headers=headers, data=data, files=files)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid patient ID", response.json()["detail"])

        # 3. Invalid file type (not PDF)
        text_file = io.BytesIO(b"some plain text")
        data = {
            "patient_id": "PAT-12345",
            "patient_phone_number": "+919876543210",
            "prescription_notes": "Take Vitamin D daily."
        }
        files = {"file": ("report.txt", text_file, "text/plain")}
        response = self.client.post("/api/v1/reports/upload", headers=headers, data=data, files=files)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Only PDF is supported", response.json()["detail"])

        # 4. Invalid PDF content (wrong signature/magic bytes)
        fake_pdf = io.BytesIO(b"NOT_A_PDF_content")
        data = {
            "patient_id": "PAT-12345",
            "patient_phone_number": "+919876543210",
            "prescription_notes": "Take Vitamin D daily."
        }
        files = {"file": ("report.pdf", fake_pdf, "application/pdf")}
        response = self.client.post("/api/v1/reports/upload", headers=headers, data=data, files=files)
        self.assertEqual(response.status_code, 400)
        self.assertIn("invalid file signature", response.json()["detail"])
        print("Input validation successfully blocked malformed fields and fake files.")

    def test_04_cors_hardening(self):
        print("\n--- Testing Layer 1: CORS Hardening ---")
        # Request from an unauthorized origin
        headers = {"Origin": "https://evil-site.com"}
        response = self.client.options("/api/v1/auth/login", headers=headers)
        # Check that origin is NOT reflected back in Access-Control-Allow-Origin
        self.assertNotEqual(response.headers.get("access-control-allow-origin"), "https://evil-site.com")
        print("CORS configuration rejected unauthorized origins.")

    def test_05_phone_number_encryption(self):
        print("\n--- Testing Layer 5: Phone Number Encryption at Rest ---")
        # Create a new patient
        new_patient = Patient(
            age_group="30-40",
            gender="TestMale"
        )
        # Set phone number using encryption wrapper
        new_patient.set_phone("+919876543210")
        self.db.add(new_patient)
        self.db.commit()

        patient_id = new_patient.patient_id

        # Query using raw SQL connection to see exactly what is stored in DB
        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT phone_number FROM patient WHERE patient_id = :id"),
                {"id": patient_id}
            )
            stored_phone = result.scalar()

        # The stored phone number must be encrypted ciphertext, not the plain text number
        self.assertNotEqual(stored_phone, "+919876543210")
        self.assertTrue(stored_phone.startswith("gAAAAA"))  # Standard Fernet token prefix
        print(f"Encrypted phone number in DB: {stored_phone}")

        # Decrypt it using the model method
        self.assertEqual(new_patient.get_phone(), "+919876543210")
        print("Phone number is securely encrypted in DB and transparently decrypted on access.")

    def test_06_audit_logging(self):
        print("\n--- Testing Layer 6: Audit Logging ---")
        # Query audit_log table to verify registration and login events were logged
        logs = self.db.query(AuditLog).order_by(AuditLog.timestamp.desc()).all()
        self.assertTrue(len(logs) > 0)
        
        event_types = [log.event_type for log in logs]
        actions = [log.action for log in logs]

        self.assertIn("AUTH", event_types)
        self.assertIn("register_success", actions)
        self.assertIn("login_success", actions)
        
        # Check that patient ID is hashed and not stored in plain text
        for log in logs:
            if log.patient_id_hash:
                self.assertNotEqual(log.patient_id_hash, "PAT-12345")
                self.assertEqual(len(log.patient_id_hash), 16) # Hashed output is 16 chars (sliced SHA-256)
        
        print("Database audit logs successfully recorded security events with anonymized patient IDs.")

    def test_07_rate_limiting(self):
        print("\n--- Testing Layer 3: API Rate Limiting ---")
        login_payload = {
            "email": "test_doctor@clinic.com",
            "password": "wrongpassword"
        }
        
        # Trigger 11 rapid requests to login (which is rate limited to 10/minute)
        throttled = False
        for i in range(15):
            response = self.client.post("/api/v1/auth/login", json=login_payload)
            if response.status_code == 429:
                throttled = True
                print(f"Successfully throttled request {i+1} with HTTP 429.")
                break
            time.sleep(0.01) # Rapid calls

        self.assertTrue(throttled, "Rate limiting did not trigger HTTP 429 after 10 requests")

    def test_08_database_persistence(self):
        print("\n--- Testing Database Persistence of Patient & Clinical Records ---")
        headers = {"Authorization": f"Bearer {self.token}"}
        
        # Upload valid report
        import uuid
        import fitz
        test_pat_id = f"PAT-TEST-{uuid.uuid4().hex[:6]}"
        test_notes = "Take 1 Vitamin D pill daily."
        
        # Generate a valid PDF stream in memory using fitz
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((50, 50), "Hemoglobin 13.5")
        page.insert_text((50, 70), "Cholesterol 180")
        page.insert_text((50, 90), "Vitamin D 32")
        pdf_bytes = doc.write()
        doc.close()
        
        pdf_file = io.BytesIO(pdf_bytes)
        data = {
            "patient_id": test_pat_id,
            "patient_phone_number": "+919876543210",
            "prescription_notes": test_notes
        }
        files = {"file": ("report.pdf", pdf_file, "application/pdf")}
        
        response = self.client.post("/api/v1/reports/upload", headers=headers, data=data, files=files)
        self.assertEqual(response.status_code, 200)
        
        # Verify db persistence
        db_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, test_pat_id)
        
        patient_rec = self.db.query(Patient).filter(Patient.patient_id == db_uuid).first()
        self.assertIsNotNone(patient_rec)
        self.assertEqual(patient_rec.get_phone(), "+919876543210")
        
        report_rec = self.db.query(Report).filter(Report.patient_id == db_uuid).order_by(Report.report_id.desc()).first()
        self.assertIsNotNone(report_rec)
        self.assertEqual(report_rec.hemoglobin, 13.5)
        self.assertEqual(report_rec.cholesterol, 180.0)
        self.assertEqual(report_rec.vitamin_d, 32.0)
        
        prescription_rec = self.db.query(Prescription).filter(Prescription.patient_id == db_uuid).order_by(Prescription.prescription_id.desc()).first()
        self.assertIsNotNone(prescription_rec)
        self.assertEqual(prescription_rec.medicine_name, test_notes)
        
        # Clean up
        self.db.delete(prescription_rec)
        self.db.delete(report_rec)
        self.db.delete(patient_rec)
        self.db.commit()
        print("Database persistence, extraction mapping, and encryption verified successfully!")

    def test_09_intern_cosignature_flow(self):
        print("\n--- Testing Medical Intern & Doctor Co-signature Flow ---")
        # Temporarily disable rate limiting for this test to avoid 429 from previous tests
        from app.core.rate_limiter import limiter
        limiter.enabled = False

        # Clean up existing intern user if left over from a previous failed run
        existing_intern = self.db.query(User).filter(User.email == "intern_test@test.com").first()
        if existing_intern:
            self.db.delete(existing_intern)
            self.db.commit()

        # 1. Register intern
        register_data = {
            "email": "intern_test@test.com",
            "password": "testpassword123",
            "full_name": "Dr. Intern",
            "role": "intern"
        }
        resp = self.client.post("/api/v1/auth/register", json=register_data)
        self.assertEqual(resp.status_code, 201)

        # Log in as intern to get token
        login_data = {
            "email": "intern_test@test.com",
            "password": "testpassword123"
        }
        resp_login = self.client.post("/api/v1/auth/login", json=login_data)
        self.assertEqual(resp_login.status_code, 200)
        intern_token = resp_login.json()["access_token"]
        intern_headers = {"Authorization": f"Bearer {intern_token}"}

        # 2. Upload report as intern
        import uuid
        import fitz
        test_pat_id = f"PAT-INT-{uuid.uuid4().hex[:6]}"
        test_notes = "Daily Vitamin D."
        
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((50, 50), "Hemoglobin 13.5")
        page.insert_text((50, 70), "Cholesterol 180")
        page.insert_text((50, 90), "Vitamin D 32")
        pdf_bytes = doc.write()
        doc.close()
        
        pdf_file = io.BytesIO(pdf_bytes)
        data = {
            "patient_id": test_pat_id,
            "patient_phone_number": "+919876543210",
            "prescription_notes": test_notes
        }
        files = {"file": ("report_intern.pdf", pdf_file, "application/pdf")}
        
        response = self.client.post("/api/v1/reports/upload", headers=intern_headers, data=data, files=files)
        self.assertEqual(response.status_code, 200)
        resp_json = response.json()
        self.assertEqual(resp_json["call_status"]["status"], "pending_cosignature")

        # 3. Check report status in DB
        db_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, test_pat_id)
        report_rec = self.db.query(Report).filter(Report.patient_id == db_uuid).first()
        self.assertIsNotNone(report_rec)
        self.assertEqual(report_rec.status, "pending_cosignature")

        # 4. Fetch pending queue as doctor
        doctor_headers = {"Authorization": f"Bearer {self.token}"}
        resp_queue = self.client.get("/api/v1/reports/pending-cosignature", headers=doctor_headers)
        self.assertEqual(resp_queue.status_code, 200)
        queue_list = resp_queue.json()
        self.assertTrue(any(item["report_id"] == str(report_rec.report_id) for item in queue_list))

        # 5. Doctor co-signs report
        cosign_payload = {"report_ids": [str(report_rec.report_id)]}
        resp_cosign = self.client.post("/api/v1/reports/cosign", headers=doctor_headers, json=cosign_payload)
        self.assertEqual(resp_cosign.status_code, 200)

        # 6. Verify status updated to completed in DB
        self.db.refresh(report_rec)
        self.assertEqual(report_rec.status, "completed")

        # Clean up
        patient_rec = self.db.query(Patient).filter(Patient.patient_id == db_uuid).first()
        prescription_rec = self.db.query(Prescription).filter(Prescription.patient_id == db_uuid).first()
        if prescription_rec:
            self.db.delete(prescription_rec)
        if report_rec:
            self.db.delete(report_rec)
        if patient_rec:
            self.db.delete(patient_rec)
            
        intern_user = self.db.query(User).filter(User.email == "intern_test@test.com").first()
        if intern_user:
            self.db.delete(intern_user)
        self.db.commit()
        
        # Restore rate limiting
        limiter.enabled = True
        print("Medical Intern verification and Attending Doctor co-signature flows verified successfully!")

if __name__ == "__main__":
    unittest.main()
