# services/feature1_executor.py

import requests
from pathlib import Path

MODEL_BASE_URL = "http://154.201.127.0:7001"
GENERATE_ENDPOINT = f"{MODEL_BASE_URL}/generate"


def run_feature1_job(job):
    """
    Submits job to model and waits for SUCCESS response.
    Does NOT download output video.
    """

    video_path = Path(job["input_video"])
    audio_path = Path(job["input_audio"])

    print("➡️ Submitting to model:")
    print(f"   Video: {video_path}")
    print(f"   Audio: {audio_path}")

    with open(video_path, "rb") as v, open(audio_path, "rb") as a:
        response = requests.post(
            GENERATE_ENDPOINT,
            files={
                "media": (video_path.name, v, "video/mp4"),
                "audio": (audio_path.name, a, "audio/wav"),
            },
            timeout=300
        )

    print("====== MODEL RESPONSE ======")
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)
    print("============================")

    if response.status_code != 200:
        raise Exception(f"Model request failed: {response.text}")

    data = response.json()

    if data.get("status") != "success":
        raise Exception(f"Model returned non-success status: {data}")

    # Return entire model response for logging/storage if needed
    return data
