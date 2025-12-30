from app.celery_app import celery_app
from app.notifications.email_utils import send_email
from app.core.config import settings

@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=10,
    retry_kwargs={"max_retries": 3},
)
def send_email_task(
    self,
    subject: str,
    body: str,
    to_emails: list[str],
):
    send_email(
        subject=subject,
        body=body,
        to_emails=to_emails,
        from_email=settings.FROM_EMAIL,
        smtp_host=settings.SMTP_HOST,
        smtp_port=settings.SMTP_PORT,
        username=settings.SMTP_USERNAME,
        password=settings.SMTP_PASSWORD,
    )


