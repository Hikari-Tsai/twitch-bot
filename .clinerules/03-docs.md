---
paths:
  - "**/*.md"
  - ".env.example"
  - ".pr_agent.toml"
  - ".github/workflows/*.yml"
  - ".github/workflows/*.yaml"
---

# Documentation And Configuration Guidelines

## Language

- Write repository documentation in Traditional Chinese unless the surrounding file is already English-only.
- Keep explanations concise and operational.
- Use exact environment variable names and command examples.

## README

- Keep the project structure section in sync with committed files that users need to understand.
- Document new setup steps, required secrets, and runtime behavior changes.
- Distinguish clearly between bot account ID (`TWITCH_BOT_ID`) and target channel owner ID (`TWITCH_OWNER_ID`).

## GitHub Actions

- Keep workflow permissions scoped to what the job needs.
- Use GitHub Secrets for API keys.
- Do not hard-code model provider keys, Twitch tokens, or account IDs.

## PR-Agent

- Keep `.pr_agent.toml` minimal and focused on settings this repository intentionally overrides.
- Prefer Traditional Chinese PR-Agent output.
- Review guidance should emphasize security, public chat behavior, cooldowns, prompt injection risk, and README or `.env.example` drift.

