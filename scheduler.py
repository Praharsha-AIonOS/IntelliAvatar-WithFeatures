# scheduler.py

import time
from services.job_repository import (
    fetch_oldest_pending_job,
    has_in_progress_job
)
from services.job_executor import execute_job


def run_scheduler():
    print("🟢 Scheduler started (STRICT SINGLE-JOB MODE)")

    while True:
        # 🔒 RULE 1: If a job is already running, DO NOTHING
        if has_in_progress_job():
            print("⏳ A job is already IN_PROGRESS. Waiting...")
            time.sleep(5)
            continue

        # 🔒 RULE 2: Fetch only QUEUED jobs
        job = fetch_oldest_pending_job()

        if not job:
            print("⏳ No queued jobs found. Waiting...")
            time.sleep(5)
            continue

        job_id = job["job_id"]
        print(f"🚀 Starting job {job_id}")

        # 🔒 RULE 3: Submit ONLY ONE job
        execute_job(job)

        print(
            f"🟡 Job {job_id} submitted to model. "
            f"Waiting for model completion..."
        )


if __name__ == "__main__":
    run_scheduler()
