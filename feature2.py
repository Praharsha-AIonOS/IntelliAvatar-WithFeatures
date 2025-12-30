# api/feature2.py

import os
import uuid
import requests
from fastapi import APIRouter, UploadFile, Form
from config.tts_config import get_voice
from services.tts_client import generate_audio

router = APIRouter(prefix="/feature2", tags=["Feature2"])

FEATURE1_ENDPOINT = "http://127.0.0.1:8000/feature1/create-job"

TEMP_AUDIO_DIR = "storage/temp_audio"
os.makedirs(TEMP_AUDIO_DIR, exist_ok=True)


@router.post("/text-to-avatar")
async def text_to_audio(
    user_id: str = Form(...),
    text: str = Form(...),
    gender: str = Form(...),
    language: str = Form("en"),
    video: UploadFile = Form(...)
):
    """
    1. Convert text → audio using TTS
    2. Forward audio + video to Feature1
    """

    # Step 1: Resolve voice
    voice = get_voice(gender)

    # Step 2: Generate temp audio
    audio_id = str(uuid.uuid4())
    temp_audio_path = os.path.join(TEMP_AUDIO_DIR, f"{audio_id}.wav")

    generate_audio(
        text=text,
        voice=voice,
        output_path=temp_audio_path
    )

    # Step 3: Forward to Feature1
    with open(temp_audio_path, "rb") as audio_file:
        response = requests.post(
            FEATURE1_ENDPOINT,
            params={"user_id": user_id},
            files={
                "video": (video.filename, await video.read(), video.content_type),
                "audio": ("tts.wav", audio_file, "audio/wav")
            }
        )

    response.raise_for_status()

    return response.json()
