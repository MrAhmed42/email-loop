import json
import sys

STATE_FILE = "state.json"

try:
    with open(STATE_FILE, "r") as f:
        state = json.load(f)
except Exception as e:
    print(f"CHECKER ERROR: Could not read {STATE_FILE}: {e}")
    # Exit code 1 keeps the loop alive to let the agent retry or fix file errors
    sys.exit(1)

status = state.get("status", "IN_PROGRESS")

# Defined Terminal States (Exit Code 0 = STOP PowerShell Loop)
SUCCESS_STATES = ["ACCEPTED"]
FAILURE_STATES = ["STOPPED_BY_RECIPIENT", "MAX_REJECTIONS_REACHED", "STUCK_NO_PROGRESS"]

if status in SUCCESS_STATES:
    print(f"CHECKER: Goal achieved -> [{status}]. Terminating loop successfully.")
    sys.exit(0)

elif status in FAILURE_STATES:
    print(f"CHECKER: Safety stop condition triggered -> [{status}]. Terminating loop to prevent failures.")
    sys.exit(0)

else:
    print(f"CHECKER: Current status -> [{status}]. Loop continues...")
    sys.exit(1)