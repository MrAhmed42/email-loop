import json
import subprocess
import sys
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("EmailCampaignTools")

@mcp.tool()
def check_inbox() -> str:
    """Checks the SENDER_EMAIL inbox for new unread replies. Returns parsed output."""
    try:
        result = subprocess.run(
            [sys.executable, "inbox_checker.py"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return json.dumps({
            "status": "ERROR",
            "error": e.stderr or "Failed to run inbox_checker.py"
        })

@mcp.tool()
def send_proposal_email(subject: str, body: str) -> str:
    """Sends a proposal or follow-up email to the lead. 
    Guarded: Will fail gracefully if state.json is already in WAITING_FOR_REPLY or ACCEPTED state.
    """
    try:
        with open("state.json", "r") as f:
            state = json.load(f)
    except FileNotFoundError:
        state = {}

    current_status = state.get("status", "")
    if current_status in ["WAITING_FOR_REPLY", "ACCEPTED", "STOPPED_BY_RECIPIENT"]:
        return json.dumps({
            "status": "SKIPPED",
            "reason": f"Email blocked by state guard. Current status is '{current_status}'."
        })

    try:
        result = subprocess.run(
            [sys.executable, "send_email.py", subject, body],
            capture_output=True,
            text=True,
            check=True
        )
        return json.dumps({
            "status": "SUCCESS",
            "output": result.stdout
        })
    except subprocess.CalledProcessError as e:
        return json.dumps({
            "status": "ERROR",
            "reason": e.stderr or "Failed to execute send_email.py"
        })

if __name__ == "__main__":
    mcp.run(transport="stdio")