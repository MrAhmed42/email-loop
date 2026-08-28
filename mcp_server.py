import json
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP("EmailCampaignTools")

@mcp.tool()
def check_inbox() -> str:
    """Checks the SENDER_EMAIL inbox for new unread replies. Returns parsed JSON results."""
    import inbox_checker
    return inbox_checker.run_inbox_check()

@mcp.tool()
def send_proposal_email(subject: str, body: str) -> str:
    """Sends a proposal or follow-up email to the lead. 
    Guarded: Will fail gracefully if state.json is already in WAITING_FOR_REPLY or ACCEPTED state.
    """
    # 1. Read state.json for Idempotency Guard
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

    # 2. Execute email send logic
    import send_email
    success = send_email.dispatch(subject, body)
    
    if success:
        return json.dumps({"status": "SUCCESS", "message": "Email sent successfully."})
    else:
        return json.dumps({"status": "ERROR", "reason": "SMTP transmission failed."})

if __name__ == "__main__":
    mcp.run(transport="stdio")