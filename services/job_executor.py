# services/job_executor.py

from services.feature1_executor import run_feature1_job
from services.job_repository import update_job_status


def execute_job(job):
    job_id = job["job_id"]

    update_job_status(job_id, "IN_PROGRESS")

    try:
        model_response = run_feature1_job(job)

        # We trust model success = completion
        update_job_status(job_id, "COMPLETED")

        print(f"🟢 Job {job_id} COMPLETED")
        print("📦 Model Response:", model_response)

    except Exception as e:
        update_job_status(job_id, "FAILED")
        print(f"🔴 Job {job_id} FAILED → {e}")
