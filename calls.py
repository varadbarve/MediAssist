from fastapi import APIRouter, Form, Response

router = APIRouter()

@router.post("/voice-webhook")
async def handle_voice_webhook(From: str = Form(...), Digits: str = Form(None)):
    """
    Example of a Twilio webhook to handle call events.
    The PRD mentions keypad interaction (DTMF). This is where that logic would live.

    This endpoint would be configured in your Twilio phone number settings.
    """
    # A TwiML response tells Twilio what to do based on keypad input.
    twiml_response = f"""
<Response>
    <Say>You are at the MediAssist webhook. You pressed {Digits if Digits else 'nothing'}.</Say>
</Response>
"""

    return Response(content=twiml_response, media_type="application/xml")