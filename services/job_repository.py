# services/job_repository.py

from db import get_db_connection

STATUS_SUBMITTED = "QUEUED"
STATUS_IN_PROGRESS = "IN_PROGRESS"
STATUS_COMPLETED = "COMPLETED"
STATUS_FAILED = "FAILED"


def fetch_oldest_pending_job():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM jobs
        WHERE status = ?
        ORDER BY created_at ASC
        LIMIT 1
    """, ("QUEUED",))

    row = cursor.fetchone()
    conn.close()

    return dict(row) if row else None



def update_job_status(job_id: str, status: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE jobs
        SET status = ?
        WHERE job_id = ?
    """, (status, job_id))

    conn.commit()
    conn.close()


def update_job_output(job_id: str, output_path: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE jobs
        SET status = ?, output_video = ?
        WHERE job_id = ?
    """, (STATUS_COMPLETED, output_path, job_id))

    conn.commit()
    conn.close()

def has_in_progress_job():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 1 FROM jobs
        WHERE status = ?
        LIMIT 1
    """, (STATUS_IN_PROGRESS,))

    exists = cursor.fetchone() is not None
    conn.close()
    return exists
