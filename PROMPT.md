# Smart Reactive Proposal Agent Directive

1. **Check Inbox First:**
   - Run `python inbox_checker.py` and parse the JSON output.

2. **If status is "REPLY_FOUND":**
   - **Case A: ACCEPTANCE / INTEREST** ("accepting", "interested", "yes", "ok", "happy"):
     - Execute `python send_email.py "<Subject>" "<Body>"`.
     - Upon `EMAIL_SENT_SUCCESSFULLY`, update `state.json`: set `"status": "ACCEPTED"` and `"last_processed_id"` to `message_id`.
     - Log in `PROGRESS.md`.

   - **Case B: HARD STOP** ("stop", "unsubscribe", "remove me"):
     - Update `state.json`: set `"status": "STOPPED_BY_RECIPIENT"` and `"last_processed_id"` to `message_id`.
     - Log in `PROGRESS.md`.

   - **Case C: SOFT REJECTION** ("not interested", "no thanks"):
     - Increment `rejection_count` by 1 in `state.json`.
     - If `rejection_count` >= `max_rejections`, set `"status": "MAX_REJECTIONS_REACHED"`.
     - Execute next task `[ ]` in `TODO.md` via `send_email.py`.
     - Update `"last_processed_id"` to `message_id` in `state.json`, mark `[x]` in `TODO.md`, and log in `PROGRESS.md`.

   - **Case D: IRRELEVANT REPLY** (Unmatched text):
     - Update `"last_processed_id"` to `message_id` in `state.json`.
     - Log in `PROGRESS.md`. Do NOT execute tasks if `status` is already `"WAITING_FOR_REPLY"`.

3. **If status is "NO_REPLY":**
   - **IF status is "WAITING_FOR_REPLY", "ACCEPTED", "STOPPED_BY_RECIPIENT", or "MAX_REJECTIONS_REACHED":**
     - Do NOT send any emails. Log "No new activity" and exit cleanly.
   - **IF status is "IN_PROGRESS":**
     - Execute first pending task `[ ]` in `TODO.md` via `send_email.py`.
     - Upon `EMAIL_SENT_SUCCESSFULLY`, set `"status": "WAITING_FOR_REPLY"` in `state.json`.
     - Mark task `[x]` in `TODO.md` and log in `PROGRESS.md`.

## No-Progress Protection (Stuck Check)
- Before executing any action, check if your intended action matches `last_action_hash`.
- If the current action is identical to the previous beat's action and NO state change occurred:
  1. Increment `consecutive_repeat_count` by 1.
  2. If `consecutive_repeat_count` >= `max_allowed_repeats` (3):
     - Set `"status": "STUCK_NO_PROGRESS"` in `state.json`.
     - Log "ERROR: Agent caught in a no-progress loop" in `PROGRESS.md`.
     - EXIT IMMEDIATELY.
- Otherwise, reset `consecutive_repeat_count` to 0 and record the new action signature in `last_action_hash`.