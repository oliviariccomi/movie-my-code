---
tags: [skill-creator]
max_turns: 60
timeout_seconds: 1800
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

I need a short video to present our internal tool "Inbox Triage" to the leadership team on Thursday. I'll talk over it live, in English, no music. What it does: incoming support emails land in a queue, a language model classifies urgency (critical, normal, low) and drafts a reply, a support agent reads the draft and approves or edits it; nothing is sent without a human. Measured so far on 120 real emails: 4 seconds per email, about 0.004 USD each, no urgent email missed in the sample. It was built in six weeks by two developers using a coding agent (Claude Code) for implementation, a second agent for code review, and a scheduled agent that posts the weekly status in Slack. Rules live in AGENTS.md, decisions in a DECISIONS.md log, and two hooks block pushes to main and secrets in files. Brand colors: navy #1B2A49, teal #1F8A8A, light grey #F2F4F7, amber #F2A900. Keep it under five minutes.
