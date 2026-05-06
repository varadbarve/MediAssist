from fastapi import APIRouter, Form, Response

router = APIRouter()

@router.post("/voice-webhook")
async def handle_voice_webhook(From: str = Form(...), Digits: str = Form(None)):
    """
    Twilio webhook to handle keypad (DTMF) interaction.
    """
    twiml_response = "<Response>"
    if Digits == "1":
        twiml_response += "<Say>Repeating the summary. Please listen carefully.</Say>"
    elif Digits == "3":
        twiml_response += "<Say>Connecting you to a medical professional. Please hold.</Say>"
    else:
        twiml_response += f"<Say>You pressed {Digits if Digits else 'nothing'}. Press 1 to repeat or 3 for a doctor.</Say>"
    twiml_response += "</Response>"

    return Response(content=twiml_response, media_type="application/xml")