# services/job_executor.py

from services.model_client import call_lipsync_model
from services.job_repository import update_job_status

STATUS_IN_PROGRESS = "IN_PROGRESS"
STATUS_FAILED = "FAILED"


def execute_job(job: dict):
    job_id = job["job_id"]
    print(f"🟡 Locking job {job_id} (IN_PROGRESS)")

    try:
        # 🔒 Lock first
        update_job_status(job_id, "IN_PROGRESS")

        print(f"🚀 Submitting job {job_id} to model")
        response = call_lipsync_model(
            job["input_video"],
            job["input_audio"]
        )

        model_job_id = response.get("job_id")
        if not model_job_id:
            raise Exception("Model did not return job_id")

        print(
            f"🟢 Job {job_id} submitted once. "
            f"Model job id: {model_job_id}"
        )

    except Exception as e:
        print(f"🔴 Job {job_id} FAILED | {e}")
        update_job_status(job_id, "FAILED")
