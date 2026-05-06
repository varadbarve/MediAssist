# MediAssist AI

MediAssist AI is an AI-powered voice assistant that automatically contacts patients after medical reports are generated, explains their reports in simple language, provides doctor-approved medication and precautionary instructions, and escalates complex cases to human doctors when necessary.

## Project Structure

- `backend/`: Python FastAPI application handling report processing, AI summarization, and voice call logic.
- `frontend/`: Next.js dashboard for hospitals and clinics to manage patients and reports.
- `base.md`: Product Requirements Document (PRD).

## Getting Started

### Backend

1. Navigate to the `backend` directory.
2. Install dependencies: `pip install -r requirements.txt`.
3. Create a `.env` file based on `.env.example`.
4. Run the server: `uvicorn app.main:app --reload`.

### Frontend

1. Navigate to the `frontend` directory.
2. Install dependencies: `npm install`.
3. Run the development server: `npm run dev`.

## Core Modules

- **Report Processing**: Extracts medical values from PDF reports.
- **AI Summarization**: Converts medical data into patient-friendly language.
- **Voice Calling**: Automated outbound calls via Twilio.
- **Doubt Resolution**: Handles basic patient questions during calls.
- **Human Escalation**: Connects patients to doctors when needed.