---
name: email-campaign-beat
description: Rules and execution steps for processing the proposal campaign beat.
---

# Email Campaign Execution Rules

1. **Inbox Triage:**
   - Run `python inbox_checker.py` to pull unread messages from `SENDER_EMAIL`.
   - Parse any incoming replies from prospects.

2. **State Updates:**
   - Update lead statuses in `state.json`.
   - Log actions taken into `PROGRESS.md` with timestamps.

3. **Follow-up Guard:**
   - Only draft or send a follow-up email if `state.json` explicitly marks a lead as `FOLLOWUP_DUE`.
   - If no reply arrived and no follow-up is due, do NOT send any email.

4. **Tone & Formatting:**
   - Emails must remain professional, concise, and non-spammy.