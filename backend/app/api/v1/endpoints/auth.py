"""
Layer 9 — Authentication API Endpoints
Register, Login, and Get Current User profile.
Rate-limited to 10 requests/minute to prevent brute-force attacks.
"""

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.audit import log_event
from app.core.rate_limiter import limiter
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.services.auth_service import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
)

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
async def register(request: Request, user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user account.
    Password is hashed with bcrypt before storage.
    """
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        log_event(
            event_type="AUTH",
            action="register_failed",
            ip_address=request.client.host if request.client else "unknown",
            details=f"Duplicate email attempt: {user_data.email}",
            status="failure"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email already exists."
        )

    # Create user with hashed password
    new_user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        full_name=user_data.full_name,
        role=user_data.role,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    log_event(
        event_type="AUTH",
        action="register_success",
        ip_address=request.client.host if request.client else "unknown",
        user_email=user_data.email,
        details=f"Role: {user_data.role}"
    )

    return new_user


@router.post("/login", response_model=Token)
@limiter.limit("10/minute")
async def login(request: Request, credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user and return a JWT access token.
    """
    client_ip = request.client.host if request.client else "unknown"

    user = db.query(User).filter(User.email == credentials.email).first()

    if not user or not verify_password(credentials.password, user.hashed_password):
        log_event(
            event_type="AUTH",
            action="login_failed",
            ip_address=client_ip,
            details=f"Failed login attempt for: {credentials.email}",
            status="failure"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated."
        )

    # Generate JWT token
    access_token = create_access_token(data={"sub": user.email})

    log_event(
        event_type="AUTH",
        action="login_success",
        ip_address=client_ip,
        user_email=user.email
    )

    return Token(
        access_token=access_token,
        user=UserResponse.model_validate(user)
    )


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """
    Get the profile of the currently authenticated user.
    Requires a valid JWT token in the Authorization header.
    """
    return current_user
