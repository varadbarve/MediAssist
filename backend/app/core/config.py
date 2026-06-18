import os
from dotenv import load_dotenv
import secrets

# Load environment variables from a .env file
load_dotenv()

# --- AI Services ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --- Database ---
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./mediassist.db")

# --- Voice Services ---
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

# --- Security ---
SECRET_KEY: str = os.getenv("SECRET_KEY", secrets.token_urlsafe(64))
ENCRYPTION_KEY: str = os.getenv("ENCRYPTION_KEY", "")
ALLOWED_ORIGINS: list = [
    origin.strip()
    for origin in os.getenv(
        "ALLOWED_ORIGINS",
        "https://medi-assist-01.vercel.app,http://localhost:3000"
    ).split(",")
]
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

# --- App ---
PROJECT_NAME: str = "MediAssist AI"
API_V1_STR: str = "/api/v1"