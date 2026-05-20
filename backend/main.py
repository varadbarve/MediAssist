from fastapi import FastAPI
from app.core.config import PROJECT_NAME, API_V1_STR, ALLOWED_ORIGINS
from app.api.v1.api import api_router
from fastapi.middleware.cors import CORSMiddleware
from app.db.base import Base
from app.db.session import engine

# --- Layer 3: Rate Limiting ---
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.rate_limiter import limiter

# --- Layer 8: Security Headers ---
from app.core.security_headers import SecurityHeadersMiddleware

# Create database tables (including new User and AuditLog tables)
Base.metadata.create_all(bind=engine)

# Run raw migrations to add status column if it does not exist
from sqlalchemy import text
with engine.connect() as conn:
    try:
        conn.execute(text("ALTER TABLE report ADD COLUMN status VARCHAR DEFAULT 'pending_review'"))
        conn.commit()
        print("[DATABASE migration] Added status column to report table successfully.")
    except Exception as e:
        pass

app = FastAPI(
    title=PROJECT_NAME,
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",
)

# --- Layer 3: Register rate limiter ---
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# --- Layer 8: Security Headers ---
app.add_middleware(SecurityHeadersMiddleware)

# --- Layer 1: CORS Hardening ---
# Only allow requests from whitelisted origins (no more "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": f"Welcome to {PROJECT_NAME}"}


app.include_router(api_router, prefix=API_V1_STR)