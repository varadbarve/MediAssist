# Product Requirements Document (PRD)

## AI Doctor Assistant – Automated Patient Follow-Up & Medical Report Explanation System

---

# 1. Product Overview

## Product Name

**MediAssist AI** *(working title)*

---

## Product Vision

Build an AI-powered voice assistant that automatically contacts patients after medical reports are generated, explains their reports in simple language, provides doctor-approved medication and precautionary instructions, answers basic follow-up questions, and escalates complex cases to human doctors when necessary.

---

## Problem Statement

Hospitals, clinics, and pathology labs spend significant time:

* Explaining routine blood reports
* Repeating medication instructions
* Answering common patient doubts
* Handling repetitive follow-up calls

This creates:

* Increased doctor workload
* Long patient wait times
* Communication gaps
* Higher operational costs

Patients also frequently:

* Forget medication schedules
* Misunderstand reports
* Ignore precautionary advice
* Need clarification after consultations

---

## Proposed Solution

An AI-powered automated calling assistant that:

1. Reads medical reports
2. Generates patient-friendly summaries
3. Calls patients automatically
4. Explains test results
5. Reads prescription instructions
6. Provides precautionary advice
7. Handles basic patient questions
8. Escalates complex queries to doctors

---

# 2. Goals & Objectives

## Primary Goals

* Reduce doctor/staff workload
* Improve patient understanding
* Improve medication adherence
* Automate routine follow-up communication
* Reduce operational costs

---

## Secondary Goals

* Create structured medical datasets
* Build scalable healthcare automation
* Improve patient engagement
* Enable future AI-assisted healthcare workflows

---

# 3. Scope

# In Scope (MVP)

## Report Processing

* Blood test report parsing
* Detection of abnormal values
* Simple report summarization

---

## Voice Calling

* Automated outbound patient calls
* AI-generated speech
* Multi-language support (future phase)

---

## Prescription Assistance

* Medication schedule explanation
* Dosage reminders
* Doctor-approved precautions

---

## Patient Interaction

* Keypad-based interaction
* Voice-based doubt clarification
* Repeat instructions feature

---

## Escalation

* Connect patient to doctor/staff
* Forward unresolved queries

---

# Out of Scope (MVP)

* Disease diagnosis
* Emergency medical advice
* Autonomous prescription generation
* Surgery/critical care recommendations
* Full AI doctor functionality

---

# 4. Target Users

## Primary Users

* Hospitals
* Clinics
* Pathology labs
* Diagnostic centers

---

## Secondary Users

* Patients
* Elderly patients
* Rural healthcare users
* Follow-up care patients

---

# 5. User Flow

# Main Workflow

```text id="fd9e4"
Lab Report Generated
        ↓
Report Uploaded to System
        ↓
AI Extracts Medical Values
        ↓
AI Generates Summary
        ↓
Prescription & Doctor Notes Attached
        ↓
Automated Call Initiated
        ↓
Patient Hears Summary
        ↓
Patient Chooses:
    1 → Understood
    2 → Ask Questions
    3 → Connect to Doctor
```

---

# 6. Functional Requirements

# 6.1 Report Processing Module

## Features

* Upload PDF reports
* OCR support for scanned reports
* Extract:

  * Hemoglobin
  * Cholesterol
  * Sugar
  * Vitamin levels
  * Other blood markers

---

## Output Example

```text id="t6j2m"
Hemoglobin is lower than normal.
Vitamin D levels are deficient.
Cholesterol levels are elevated.
```

---

# 6.2 AI Summarization Module

## Features

* Convert medical data into patient-friendly language
* Avoid complex medical terminology
* Highlight:

  * High values
  * Low values
  * Normal values

---

## Safety Rules

AI must:

* NOT diagnose diseases
* NOT prescribe new medicines
* NOT override doctor advice

---

# 6.3 Prescription Guidance Module

## Features

* Read doctor-provided instructions
* Explain:

  * Medicine timing
  * Dosage
  * Food restrictions
  * Lifestyle precautions

---

## Example

```text id="0g8pr"
Take Vitamin D tablets once daily after breakfast.
Avoid oily and spicy food for 5 days.
Drink plenty of water.
```

---

# 6.4 AI Voice Calling Module

## Features

* Outbound automated calls
* Text-to-speech generation
* Voice playback
* Retry failed calls

---

## User Inputs

* Keypad interaction (DTMF)
* Voice response detection

---

# 6.5 Doubt Resolution Module

## Features

* Speech-to-text conversion
* Basic FAQ answering
* Clarification requests

---

## Allowed Questions

* “When should I take medicine?”
* “Can I take medicine after food?”
* “What foods should I avoid?”

---

## Restricted Questions

* “Do I have cancer?”
* “Should I stop insulin?”
* “Can I ignore the prescription?”

For restricted questions:

```text id="d0vwb"
Please consult your doctor directly.
Would you like to connect with a medical professional?
```

---

# 6.6 Human Escalation Module

## Features

* Transfer call to doctor/staff
* Generate callback requests
* Store unresolved queries

---

# 7. Non-Functional Requirements

| Category     | Requirement                    |
| ------------ | ------------------------------ |
| Reliability  | 99% successful call handling   |
| Scalability  | Support thousands of calls/day |
| Security     | Encrypted patient data         |
| Compliance   | HIPAA-like design principles   |
| Latency      | <3 sec response time           |
| Availability | 24/7 service                   |

---

# 8. System Architecture

# High-Level Architecture

```text id="j1l3c"
Frontend Dashboard
        ↓
Backend API Server
        ↓
AI Processing Layer
        ↓
Voice Call Engine
        ↓
Patient Phone Call
```

---

# Components

## Frontend

* React / Next.js dashboard

---

## Backend

* Python FastAPI

---

## Database

* PostgreSQL

---

## AI Layer

* Google Gemini API (gemini-1.5-flash / gemini-pro)

---

## Voice Services

* Twilio Voice API

---

## Speech-to-Text

* Twilio Built-in Speech / DTMF keypad

---

## Text-to-Speech

* Edge TTS (edge-tts python package)

---

# 9. Database Design (Basic)

# Patient Table

| Field        | Type      |
| ------------ | --------- |
| patient_id   | UUID      |
| age_group    | String    |
| gender       | String    |
| phone_number | Encrypted |

---

# Report Table

| Field       | Type  |
| ----------- | ----- |
| report_id   | UUID  |
| patient_id  | FK    |
| hemoglobin  | Float |
| cholesterol | Float |
| vitamin_d   | Float |

---

# Prescription Table

| Field           | Type   |
| --------------- | ------ |
| prescription_id | UUID   |
| patient_id      | FK     |
| medicine_name   | String |
| dosage          | String |
| timing          | String |

---

# User Table

| Field           | Type    |
| --------------- | ------- |
| id              | Integer |
| email           | String  |
| hashed_password | String  |
| full_name       | String  |
| role            | String  |
| is_active       | Boolean |
| created_at      | DateTime|

---

# Audit Log Table

| Field           | Type    |
| --------------- | ------- |
| id              | Integer |
| timestamp       | DateTime|
| event_type      | String  |
| ip_address      | String  |
| patient_id_hash | String  |
| user_email      | String  |
| action          | String  |
| details         | Text    |
| status          | String  |

---

# 10. AI Safety Requirements

## AI Must Never:

* Diagnose diseases autonomously
* Recommend stopping medications
* Provide emergency advice
* Generate unsupported medical claims

---

## AI Must:

* Follow doctor-provided instructions
* Use predefined medical boundaries
* Escalate uncertain situations

---

# 11. Privacy & Compliance

## Data Protection

* Remove personally identifiable information
* Encrypt sensitive data
* Role-based access control

---

## Audit Logging

Track:

* Call history
* AI responses
* Escalations
* Patient interactions

---

# 12. Future Roadmap

# Phase 1

* Blood report explanation
* Basic calling system

---

# Phase 2

* Multi-language support
* WhatsApp integration
* SMS reminders

---

# Phase 3

* Advanced conversational AI
* Smart patient follow-ups
* Personalized health recommendations

---

# Phase 4

* Predictive healthcare analytics
* ML-based risk assessment
* Longitudinal patient insights

---

# 13. Risks & Challenges

| Risk                     | Mitigation                     |
| ------------------------ | ------------------------------ |
| AI hallucination         | Strict prompt engineering      |
| Incorrect medical advice | Doctor-only instruction source |
| Poor speech recognition  | Confidence thresholds          |
| Legal concerns           | Human escalation system        |
| Data privacy issues      | Encryption & anonymization     |

---

# 14. Success Metrics

| Metric                     | Target |
| -------------------------- | ------ |
| Successful calls           | >90%   |
| Patient understanding rate | >85%   |
| Reduced manual follow-ups  | >50%   |
| AI escalation accuracy     | >95%   |
| Patient satisfaction       | >80%   |

---

# 15. MVP Timeline

| Week | Deliverable          |
| ---- | -------------------- |
| 1    | Report extraction    |
| 2    | AI summarization     |
| 3    | Prescription parsing |
| 4    | Voice generation     |
| 5    | Automated calling    |
| 6    | Doubt handling       |
| 7    | Human escalation     |
| 8    | Testing & deployment |

---

# 16. Conclusion

MediAssist AI aims to streamline patient communication by automating repetitive healthcare follow-ups while maintaining doctor oversight and patient safety.

The system is designed as:

* an AI-assisted healthcare communication platform,
* not a replacement for doctors.

The product focuses on:

* operational efficiency,
* patient clarity,
* healthcare accessibility,
* and scalable medical workflow automation.

---

# 17. Version History

## Version 1.0.1
Optimized the medical PDF extraction parser for high-accuracy blood marker parsing.

## Version 1.0.2
Enhanced AI response synthesis confidence checks and prompt guard parameter configurations.

## Version 1.0.3
Hardened system security middleware, implemented database-backed logging, and updated CORS policies.

## Version 1.0.4
Introduced "Patient" role for public registration with balanced 2x2 selection layout and added show/hide password toggles on authentication forms.

