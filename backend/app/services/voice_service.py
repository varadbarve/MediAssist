import os
import edge_tts
import asyncio
import uuid

def make_automated_call(phone_number: str, script: str):
    """
    Simulates an automated call using high-quality Microsoft Edge voices (FREE & UNLIMITED).
    """
    print(f"[LOG] Generating premium voice for: {phone_number}")

    output_dir = "temp_calls"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    audio_filename = f"call_{uuid.uuid4().hex[:8]}.mp3"
    file_path = os.path.join(output_dir, audio_filename)
    
    # We use a professional sounding female voice (Emma)
    voice = "en-GB-SoniaNeural" 

    try:
        # edge-tts is asynchronous, so we run it in a small event loop
        async def generate():
            communicate = edge_tts.Communicate(script, voice)
            await communicate.save(file_path)
        
        asyncio.run(generate())
        status_msg = "Premium voice simulation complete."
    except Exception as e:
        print(f"[ERROR] edge-tts Failed: {e}")
        status_msg = "Audio generation unavailable."
        audio_filename = None

    return {
        "status": "success", 
        "mode": "edge_premium",
        "audio_file": audio_filename,
        "message": status_msg
    }