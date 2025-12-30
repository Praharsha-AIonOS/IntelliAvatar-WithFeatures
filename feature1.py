# feature1.py

from fastapi import APIRouter, UploadFile, File, Query
from datetime import datetime
import uuid
import os

from db import get_db_connection

router = APIRouter(prefix="/feature1", tags=["Feature1"])

UPLOAD_DIR = "storage/uploads"
OUTPUT_DIR = "storage/outputs"


@router.post("/create-job")
async def create_job(
    user_id: str = Query(...),
    video: UploadFile = File(...),
    audio: UploadFile = File(...)
):
    job_id = str(uuid.uuid4())
    created_at = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create job directory
    job_dir = os.path.join(UPLOAD_DIR, job_id)
    os.makedirs(job_dir, exist_ok=True)

    # Paths
    video_path = os.path.join(job_dir, f"{job_id}.mp4")
    audio_path = os.path.join(job_dir, f"{job_id}.wav")
    output_path = os.path.join(OUTPUT_DIR, f"{job_id}.mp4")

    # Save files
    with open(video_path, "wb") as v:
        v.write(await video.read())

    with open(audio_path, "wb") as a:
        a.write(await audio.read())

    # Insert into SQL
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO jobs (
            job_id, user_id, input_video, input_audio,
            output_video, status, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            job_id,
            user_id,
            video_path,
            audio_path,
            output_path,
            "QUEUED",
            created_at
        )
    )

    conn.commit()
    conn.close()

    return {
        "job_id": job_id,
        "user_id": user_id,
        "input_video": video_path.replace("\\", "/"),
        "input_audio": audio_path.replace("\\", "/"),
        "output_video": output_path.replace("\\", "/"),
        "status": "QUEUED",
        "created_at": created_at
    }


from db import get_db_connection

@router.get("/jobs")
def list_jobs():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM jobs ORDER BY created_at DESC")
    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]

