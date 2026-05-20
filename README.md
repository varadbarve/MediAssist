# MediAssist AI — Smart Healthcare Follow-Up & Security-Hardened Assistant

MediAssist AI is an enterprise-grade, secure, AI-powered healthcare communication platform. The system automatically extracts key clinical markers from uploaded PDF medical reports, generates patient-friendly explanations in simple language, runs outbound voice call simulations to walk patients through their test summaries and prescriptions, and handles doubt resolution while enforcing strict healthcare guardrails and user authentication.

---

## 🚀 Key Features

### 🎙️ Outbound Voice Follow-Up
* **Automated Voice Calls:** Automatically triggers outbound calls using Twilio voice services to explain reports.
* **Smart Doubt Resolution:** Interactive keypad and speech-to-text response processing to clarify patient questions.
* **Safe Escalation:** Detects high-risk symptoms or out-of-scope medical questions and routes them to staff/doctors.

### 🧠 Medical Report Extraction & AI Summarization
* **Clinical Report Parsing:** High-accuracy PDF extraction of key blood markers (Hemoglobin, Cholesterol, Sugar, Vitamin D, etc.).
* **Patient-Friendly Summarization:** Translates complex medical terms into simple, actionable summaries.
* **Prescription Explanations:** Communicates dosages, timing, food restrictions, and lifestyle precautions.

### 🛡️ 9-Layer Enterprise Security Framework
1. **Layer 1 — CORS Hardening:** Strictly limits CORS access to trusted production origins.
2. **Layer 2 — Security Headers:** Hardens the application via HTTP headers (`X-Frame-Options`, `X-Content-Type-Options`, `Content-Security-Policy`, etc.).
3. **Layer 3 — API Rate Limiting:** Throttles clients using IP-based request limits to mitigate brute-force and DDoS attacks.
4. **Layer 4 — Input Validation & Sanitization:** Validates emails, passwords, and file uploads against rigorous schema validators.
5. **Layer 5 — Encryption at Rest:** Encrypts patient phone numbers using AES-256 (Fernet) encryption keys before database storage.
6. **Layer 6 — Audit Logging:** Retains file-based and database-persisted trails of auth and data actions with anonymized patient IDs.
7. **Layer 7 — API Key Protection:** Restricts backend secrets and API keys to environment injection.
8. **Layer 8 — Prompt Injection Guard:** Filters input queries to intercept and neutralize jailbreaks or prompt injection attacks.
9. **Layer 9 — User Authentication System:** Implements secure JWT bearer token authentication with direct `bcrypt` password hashing.

---

## 📂 Project Structure

```text
├── backend/                  # FastAPI Application
│   ├── app/
│   │   ├── api/              # API Endpoints (Auth, Calls, Reports)
│   │   ├── core/             # Configuration, Encryption, Security & Audit Logs
│   │   ├── models/           # SQLAlchemy DB Models (User, AuditLog)
│   │   ├── schemas/          # Pydantic Schemas (Request/Response validation)
│   │   ├── services/         # AI Summarization, Voice calls, PDF extraction
│   │   └── db/               # Database Connection & Session Setup
│   ├── requirements.txt      # Python Dependencies
│   └── test_security.py      # Automated Security Verification Test Suite
│
├── frontend/                 # Next.js Application
│   ├── src/
│   │   ├── app/              # Next.js App Router (Dashboard, Login, Register)
│   │   └── lib/              # Client-side Auth Utilities & API Helpers
│   ├── public/               # Static assets & Custom brand icon
│   └── tsconfig.json         # TypeScript configuration
│
├── base.md                   # Product Requirements Document (PRD)
└── variables.me              # Project Variables Cheat-Sheet
```

---

## 🛠️ Tech Stack

* **Frontend:** Next.js (App Router), TypeScript, TailwindCSS, Framer Motion, Lucide Icons.
* **Backend:** FastAPI, Python, SQLAlchemy.
* **Database:** Neon PostgreSQL (Cloud Production) / SQLite (Local Development fallback).
* **AI & Telephony:** Gemini API (Report Analysis), Twilio Voice (Call Simulations).

---

## ⚙️ Getting Started

### 📋 Prerequisites
* Python 3.10+
* Node.js 18+

### 🔑 Configuration (Environment Variables)

Create a `.env` file in the `backend/` directory:
```env
# Database Settings
DATABASE_URL="postgresql://user:pass@host/dbname?sslmode=require"

# Security Keys (Generate via cryptography Fernet)
SECRET_KEY="your-jwt-signing-secret"
ENCRYPTION_KEY="your-fernet-key-for-database-fields"

# LLM Config
GEMINI_API_KEY="your-gemini-api-key"

# Twilio (Optional/Simulated)
TWILIO_ACCOUNT_SID="your-twilio-sid"
TWILIO_AUTH_TOKEN="your-twilio-auth-token"
TWILIO_PHONE_NUMBER="your-twilio-phone-number"
```

### 1. Run Backend Server
```bash
cd backend

# Setup virtual environment
python -m venv .venv
# Activate virtual environment (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations / Run FastAPI app
uvicorn app.main:app --reload
```

### 2. Run Frontend Dashboard
```bash
cd frontend

# Install dependencies
npm install

# Run the development environment
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) to view the client-side panel.

---

## 🧪 Security & Verification Tests
To run the automated integration test suite validating security middleware, hashing, database persistence, rate-limiting, and JWT authentication:
```bash
cd backend
python test_security.py
```

---

## 📜 Version History
Refer to the [PRD](file:///c:/Users/Asus/Mediassist/base.md) for detailed version histories.
* **v1.0.1** — Medical report parsing optimizations.
* **v1.0.2** — Prompt guard filters and confidence checks.
* **v1.0.3** — Security middleware & DB audit log persistence.
* **v1.0.4** — Patient registration support, balanced grid selection, and show/hide password controls.