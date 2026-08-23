import imaplib
import email
import json
import os
import re
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
STATE_FILE = "state.json"

def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    return re.sub(cleanr, '', raw_html).strip()

def extract_body(msg):
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                payload = part.get_payload(decode=True)
                if payload:
                    body = payload.decode(errors="ignore").strip()
                    break
            elif content_type == "text/html" and not body:
                payload = part.get_payload(decode=True)
                if payload:
                    body = clean_html(payload.decode(errors="ignore"))
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            body = payload.decode(errors="ignore").strip()
            if msg.get_content_type() == "text/html":
                body = clean_html(body)
    return body

def get_last_processed_id():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                data = json.load(f)
                return str(data.get("last_processed_id"))
        except Exception:
            return None
    return None

def get_latest_reply():
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(SENDER_EMAIL, SENDER_PASSWORD)
        mail.select("inbox")

        status, messages = mail.search(None, f'FROM "{RECIPIENT_EMAIL}"')
        email_ids = messages[0].split()

        if not email_ids:
            print(json.dumps({"status": "NO_REPLY"}))
            return

        latest_id = email_ids[-1].decode("utf-8")
        last_processed_id = get_last_processed_id()

        if last_processed_id and str(last_processed_id) == str(latest_id):
            print(json.dumps({"status": "NO_REPLY"}))
            return

        status, data = mail.fetch(latest_id.encode("utf-8"), "(RFC822)")

        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                body = extract_body(msg)

                output = {
                    "status": "REPLY_FOUND",
                    "message_id": latest_id,
                    "subject": str(msg.get("Subject")),
                    "body": body if body else "(NO_BODY_FOUND)"
                }
                print(json.dumps(output, indent=2))
                return

    except Exception as e:
        print(json.dumps({"status": "ERROR", "error": str(e)}))

if __name__ == "__main__":
    get_latest_reply()