import sys
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

# Load variables from .env file if present (Local environment)
load_dotenv()

# Read variables (Works for both local .env and GitHub Actions Secrets)
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

if not SENDER_EMAIL or not SENDER_PASSWORD:
    raise ValueError("Missing SENDER_EMAIL or SENDER_PASSWORD environment variables.")

RECIPIENT_EMAIL = "nabi03343429210@gmail.com"

def send_email(subject, body):
    # Convert literal backslash-n sequences into real newlines
    formatted_body = body.replace("\\n", "\n")

    msg = MIMEText(formatted_body, "plain", "utf-8")
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python send_email.py \"<subject>\" \"<body>\"")
        sys.exit(1)

    subject_arg = sys.argv[1]
    body_arg = sys.argv[2]

    try:
        send_email(subject_arg, body_arg)
        print("EMAIL_SENT_SUCCESSFULLY")
    except Exception as e:
        print(f"EMAIL_FAILED: {e}")