from celery import Celery
import os
from config.settings import settings

celery_app = Celery(
    "aerosense_worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=True,
)

@celery_app.task(name="generate_report_task")
def generate_report_task(report_type: str, zone_id: int):
    # This is a placeholder for actual report generation logic
    # In a full implementation, this would query the DB and write a PDF/CSV to S3/Disk
    print(f"Generating {report_type} report for zone {zone_id}...")
    import time
    time.sleep(2)
    return {"status": "completed", "report_url": f"/downloads/report_{zone_id}.{report_type}"}

@celery_app.task(name="send_notification_task")
def send_notification_task(message: str, type: str):
    print(f"Sending notification: [{type}] {message}")
    return {"status": "sent"}
