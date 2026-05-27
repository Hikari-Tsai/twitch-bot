# Codex Review Guide

This repository is a Python Twitch chat bot that listens to Twitch EventSub chat
messages and uses the OpenAI Responses API to generate short public replies.

Use this guide when reviewing changes in this repo.

## Review Language

- Write review comments in Traditional Chinese.
- Lead with concrete risks, bugs, regressions, missing tests, or security issues.
- Avoid style-only suggestions unless they affect correctness, maintainability, or user safety.

## High-Risk Areas

- Secrets must never be committed, logged, printed, or included in examples:
  - `OPENAI_API_KEY`
  - `TWITCH_TOKEN`
  - `TWITCH_CLIENT_SECRET`
  - `.env`
  - `prompt/system_prompt.txt`
  - local token/cache files
- Twitch auth changes must preserve the relationship between:
  - `TWITCH_TOKEN`
  - `TWITCH_BOT_ID`
  - `TWITCH_OWNER_ID`
  - required scopes `user:read:chat` and `user:write:chat`
- Public chat replies must avoid spam:
  - keep global and per-user cooldown behavior intact
  - preserve ignore rules for commands, URLs, long messages, and blacklist users
  - keep reply probability and force-trigger behavior understandable
- LLM output must remain bounded:
  - preserve `MAX_INPUT_LENGTH` and `MAX_REPLY_LENGTH`
  - avoid changes that make prompt injection easier
  - avoid exposing private prompt or environment data in replies

## Python Review Checklist

- Confirm new environment variables are documented in both `.env.example` and
  `README.md`.
- Check that numeric environment variables fail clearly or have safe defaults.
- Check network calls for timeouts and useful errors.
- Check that Twitch EventSub handlers do not block unnecessarily.
- Check that user-visible reply behavior is deterministic enough to debug.
- Prefer small, local fixes over broad rewrites.

## GitHub Actions Review Checklist

- Confirm workflow permissions are no broader than needed.
- Prefer pinned action versions or stable tags over moving branches when possible.
- Do not expose secrets through logs, PR comments, command output, or debug flags.
- Ensure PR automation does not create duplicate pull requests or recursive workflow
  behavior.

## Documentation Expectations

- If behavior changes, update `README.md`.
- If configuration changes, update `.env.example`.
- If prompt setup changes, update `prompt/system_prompt.txt.example`.
- Do not document real secrets or local-only values.

## Local Verification

When practical, run the narrowest relevant checks:

```bash
python -m py_compile main.py
```

If dependencies are installed and the change affects runtime behavior, prefer a
focused manual check over broad speculative changes.
