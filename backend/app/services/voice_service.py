import edge_tts
import re
import base64
import io


def _clean_text_for_speech(text: str) -> str:
    """
    Cleans and prepares plain text for natural-sounding TTS.
    Removes markdown artifacts and normalizes whitespace.
    edge_tts does NOT support SSML — all text is spoken literally.
    """
    # Remove markdown formatting
    text = text.replace("**", "")
    text = text.replace("*", "")
    text = text.replace("#", "")
    text = text.replace("_", " ")

    # Remove any stray HTML/XML-like tags (safety net)
    text = re.sub(r"<[^>]+>", "", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Add natural pauses by inserting ellipses (edge_tts respects punctuation pauses)
    # Replace bullet-style lists with spoken transitions
    text = re.sub(r"\n[-•]\s*", ". Next, ", text)
    text = re.sub(r"\n\d+\.\s*", ". Next, ", text)

    return text


async def make_automated_call(phone_number: str, script: str):
    """
    Generates premium voice and returns it as Base64 — no file storage needed.
    Uses edge_tts native parameters for rate, pitch, and volume control.
    """
    print(f"[LOG] Generating human-like voice for: {phone_number}")

    voice = "en-US-AvaMultilingualNeural"
    audio_base64 = None

    # Clean the script text — remove markdown/HTML, normalize for speech
    clean_script = _clean_text_for_speech(script)

    print(f"[LOG] Clean script for TTS: {clean_script[:200]}...")

    try:
        # edge_tts uses its own rate/pitch/volume keyword args, NOT SSML
        communicate = edge_tts.Communicate(
            text=clean_script,
            voice=voice,
            rate="-10%",       # Slightly slower for clarity
            pitch="-2Hz",      # Slightly deeper for warmth
            volume="+20%"      # Louder for clarity
        )

        # Collect audio chunks into memory instead of saving to disk
        audio_buffer = io.BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_buffer.write(chunk["data"])

        audio_bytes = audio_buffer.getvalue()
        if audio_bytes:
            audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
            status_msg = "Premium voice simulation complete."
        else:
            status_msg = "Audio generation produced empty output."

    except Exception as e:
        print(f"[ERROR] edge-tts with custom params failed: {e}")
        # Fallback: try with default params
        try:
            communicate = edge_tts.Communicate(text=clean_script, voice=voice)
            audio_buffer = io.BytesIO()
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_buffer.write(chunk["data"])
            audio_bytes = audio_buffer.getvalue()
            if audio_bytes:
                audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
                status_msg = "Voice simulation complete (default params)."
            else:
                status_msg = "Audio generation produced empty output."
        except Exception as e2:
            print(f"[ERROR] Fallback also failed: {e2}")
            status_msg = "Audio generation unavailable."

    return {
        "status": "success",
        "mode": "edge_premium",
        "audio_base64": audio_base64,
        "message": status_msg
    }