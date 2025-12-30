import smtplib
from email.message import EmailMessage
from typing import List

def send_email(
    subject: str,
    body: str,
    to_emails: List[str],
    from_email: str,
    smtp_host: str,
    smtp_port: int,
    username: str,
    password: str,
):
    message = EmailMessage()
    message["From"] = from_email
    message["To"] = ", ".join(to_emails)
    message["Subject"] = subject
    message.set_content(body)

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(username, password)
        server.send_message(message)
