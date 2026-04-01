# Patient Interoperability Gateway (PIGW)

# Overview

This project implements a Django-based microservice designed to ingest FHIR Patient data, process it securely, and expose sanitized patient information via REST APIs.

The system focuses on handling sensitive healthcare data with proper encryption, validation, and audit logging.

---

# Tech Stack

* Python 3.10+
* Django & Django REST Framework
* PostgreSQL
* Cryptography (Fernet encryption)

---

# Setup Instructions

# 1. Clone the Repository

```bash
git clone https://github.com/setu666h/pigw-healthcare-service.git
cd pigw-healthcare-service
```

# 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

# 3. Install Dependencies

```bash
pip install -r requirements.txt
```

# 4. Configure Database

Update PostgreSQL credentials in `settings.py`.

# 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

# 6. Run Server

```bash
python manage.py runserver
```

---

# API Endpoints

# Patient Intake API

**POST** `/api/v1/patient-intake/`

* Accepts FHIR Patient JSON
* Validates payload
* Rejects patients under 18
* Encrypts sensitive data before storage

---

# Patient Retrieval API

**GET** `/api/v1/patients/<patient_id>/`

* Retrieves patient data
* Decrypts sensitive fields
* Masks SSN before returning response
* Logs access details (audit logging)

---

# Security Design

* Sensitive fields like SSN are encrypted using Fernet symmetric encryption
* Encrypted data is stored in the database
* Decryption happens only during retrieval
* SSN is masked before being exposed via API

# Design Decision:

Fernet was chosen due to its simplicity and built-in authentication for secure encryption and decryption.

⚠️ Note:
For this implementation, the encryption key is hardcoded for simplicity. In a production system, it should be securely managed using environment variables or a secrets manager.

---

# Audit Logging

Every access to the patient retrieval endpoint is logged with:

* Timestamp
* IP address
* User (anonymous or authenticated)

This ensures traceability and supports compliance requirements.

---

# Business Rules

* Patients under 18 are rejected
* Raw JSON payload is stored for auditing
* Sensitive data is never exposed in plain form

---

# Future Improvements

* Implement asynchronous processing using Celery
* Add authentication and authorization (JWT)
* Dockerize the application
* Add unit and integration tests

---

# Testing

```bash
python manage.py test
```

---

# Notes

This implementation focuses on correctness, security, and clarity of design rather than production-level completeness.
