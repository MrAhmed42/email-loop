---
name: email-campaign
description: Automated email proposal campaign handler using official MCP tools.
---

# Execution Workflow

1. Call `check_inbox` MCP tool to fetch recent unread client messages.
2. If a reply is received, process state according to rules in `state.json`.
3. If a follow-up is due, call `send_proposal_email` with appropriate subject and body.
4. Update `state.json` and `PROGRESS.md` with execution results.