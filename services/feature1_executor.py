# services/feature1_executor.py

import requests
from pathlib import Path

MODEL_ENDPOINT = "http://154.201.127.0:7001/generate"


def run_feature1_job(job):
    """
    job = dict fetched from DB
    {
        job_id,
        input_video,
        input_audio,
        output_video
    }
    """

    video_path = Path(job["input_video"])
    audio_path = Path(job["input_audio"])

    with open(video_path, "rb") as v, open(audio_path, "rb") as a:
        response = requests.post(
            MODEL_ENDPOINT,
            files={
                "media": ("input.mp4", v, "video/mp4"),
                "audio": ("input.wav", a, "audio/wav")
            }
        )

    if response.status_code != 200:
        raise Exception("Model execution failed")

    # Save output video
    output_path = Path(job["output_video"])
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "wb") as f:
        f.write(response.content)

    return str(output_path)


