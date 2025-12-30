# services/tts_client.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
SARVAM_TTS_ENDPOINT = "https://api.sarvam.ai/v1/text-to-speech"


def generate_audio(text: str, voice: str, output_path: str):
    """
    Converts text to speech using Sarvam TTS
    Saves audio as .wav
    """

    if not SARVAM_API_KEY:
        raise RuntimeError("SARVAM_API_KEY not found in environment")

    headers = {
        "Authorization": f"Bearer {SARVAM_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "voice": voice,
        "format": "wav"
    }

    response = requests.post(
        SARVAM_TTS_ENDPOINT,
        headers=headers,
        json=payload,
        timeout=30
    )

    # 🔴 Important debug if something goes wrong
    if response.status_code != 200:
        print("Sarvam TTS error:")
        print("Status:", response.status_code)
        print("Response:", response.text)

    response.raise_for_status()

    with open(output_path, "wb") as f:
        f.write(response.content)

    return output_path
