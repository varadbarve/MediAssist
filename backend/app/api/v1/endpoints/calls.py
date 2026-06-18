"""
Calls endpoint — Protected with:
- Layer 2: Twilio webhook signature verification
- Layer 3: Rate limiting (30/min)
- Layer 6: Audit logging
"""

from fastapi import APIRouter, Form, Response, Request, HTTPException
from app.core.rate_limiter import limiter
from app.core.audit import log_event
from app.core.config import TWILIO_AUTH_TOKEN

router = APIRouter()


def _verify_twilio_signature(request: Request, form_params: dict) -> bool:
    """
    Verify that an incoming webhook request was genuinely sent by Twilio.
    Uses Twilio's RequestValidator to check the X-Twilio-Signature header.
    Returns True if verification passes or if Twilio is not configured (dev mode).
    """
    # Skip verification if Twilio credentials are not configured (development)
    if not TWILIO_AUTH_TOKEN or TWILIO_AUTH_TOKEN == "your_twilio_auth_token":
        return True

    try:
        from twilio.request_validator import RequestValidator
        validator = RequestValidator(TWILIO_AUTH_TOKEN)

        # Get the signature from headers
        signature = request.headers.get("X-Twilio-Signature", "")
        if not signature:
            print("[SECURITY] Missing X-Twilio-Signature header.")
            return False

        # Reconstruct the full URL (Twilio uses the public URL to compute the signature)
        url = str(request.url)

        # Validate using the form parameters and signature
        is_valid = validator.validate(url, form_params, signature)
        if not is_valid:
            print(f"[SECURITY] Twilio signature validation failed for URL: {url}")
        return is_valid

    except ImportError:
        print("[SECURITY] Twilio library not installed — skipping signature verification.")
        return True
    except Exception as e:
        print(f"[SECURITY] Twilio verification error: {e}")
        return False


@router.post("/voice-webhook")
@limiter.limit("30/minute")
async def handle_voice_webhook(request: Request, From: str = Form(...), Digits: str = Form(None)):
    """
    Twilio webhook to handle keypad (DTMF) interaction.
    Verifies the request signature to prevent unauthorized access.
    """
    client_ip = request.client.host if request.client else "unknown"

    # Build form params dict for signature verification
    form_params = {"From": From}
    if Digits is not None:
        form_params["Digits"] = Digits

    # --- Layer 2: Verify Twilio signature ---
    if not _verify_twilio_signature(request, form_params):
        log_event(
            event_type="WEBHOOK",
            action="signature_verification_failed",
            ip_address=client_ip,
            details=f"Unauthorized webhook attempt from {From}",
            status="failure"
        )
        raise HTTPException(status_code=403, detail="Invalid Twilio signature.")

    # --- Layer 6: Audit log ---
    log_event(
        event_type="WEBHOOK",
        action="dtmf_received",
        ip_address=client_ip,
        details=f"From: ***{From[-4:] if len(From) > 4 else 'N/A'}, Digits: {Digits or 'none'}"
    )

    twiml_response = "<Response>"
    if Digits == "1":
        twiml_response += "<Say>Repeating the summary. Please listen carefully.</Say>"
        log_event(event_type="CALL", action="repeat_requested", ip_address=client_ip)
    elif Digits == "3":
        twiml_response += "<Say>Connecting you to a medical professional. Please hold.</Say>"
        log_event(
            event_type="ESCALATION",
            action="doctor_connect_requested",
            ip_address=client_ip,
            details=f"Patient requested doctor connection"
        )
    else:
        twiml_response += f"<Say>You pressed {Digits if Digits else 'nothing'}. Press 1 to repeat or 3 for a doctor.</Say>"
    twiml_response += "</Response>"

    return Response(content=twiml_response, media_type="application/xml")