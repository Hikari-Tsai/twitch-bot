# Project Context

This repository is a Python Twitch chat bot.

The bot listens to Twitch chat through TwitchIO EventSub and generates short public replies through the OpenAI Responses API.

## Core Files

- `main.py` contains the bot runtime, Twitch EventSub subscription, reply decision logic, OpenAI calls, cooldowns, and logging.
- `.env.example` documents configuration variables. Do not add real secrets to it.
- `prompt/system_prompt.txt.example` is the committed prompt template.
- `prompt/system_prompt.txt` is local-only and may contain private behavior instructions.
- `.github/workflows/pr-agent.yml` configures PR-Agent for GitHub pull requests.
- `.pr_agent.toml` configures PR-Agent behavior.

## Project Constraints

- Keep implementation simple unless a change clearly benefits from splitting modules.
- Preserve TwitchIO EventSub behavior unless the task explicitly changes how chat messages are received.
- Treat Twitch chat replies as public user-facing output.
- Keep replies short, bounded, and appropriate for live chat.
- When adding or changing environment variables, update `.env.example` and `README.md`.
- When changing user-visible behavior, update `README.md`.

## Security

- Never read, print, commit, or expose values from `.env`, `prompt/system_prompt.txt`, `.tio.tokens.json`, or API token files.
- Do not log `OPENAI_API_KEY`, `TWITCH_TOKEN`, `TWITCH_CLIENT_SECRET`, or OAuth validation responses containing sensitive data.
- Do not weaken checks around Twitch token scopes or `TWITCH_BOT_ID` ownership without a specific reason.

