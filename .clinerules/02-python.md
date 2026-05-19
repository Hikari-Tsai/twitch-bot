---
paths:
  - "**/*.py"
---

# Python Guidelines

## Style

- Use Python 3.10-compatible syntax.
- Prefer standard library helpers before adding dependencies.
- Keep functions small and named around behavior, not implementation details.
- Use type hints for new public helpers and non-obvious return values.
- Avoid broad refactors when fixing a narrow issue.

## Twitch Bot Behavior

- Keep ignore checks, cooldown checks, reply probability, LLM filter, and final reply generation easy to reason about.
- Do not send a Twitch reply until all ignore, cooldown, probability, and LLM filter checks have passed.
- Update `last_global_reply_at` and `last_user_reply_at` only after a message is successfully sent.
- Preserve protection against bot self-replies.
- Keep message length limits enforced before sending replies.

## OpenAI Calls

- Use the existing OpenAI Responses API client pattern unless the task requires a different API.
- Keep system prompts separate from user chat content.
- Treat Twitch chat messages as untrusted user input.
- When parsing model output as JSON, handle malformed output defensively.

## Testing And Verification

- Prefer focused tests or small pure helper checks when changing decision logic.
- At minimum, run a syntax check such as `python3 -m py_compile main.py` after Python edits.
- Do not require live Twitch or OpenAI credentials for local verification unless the user explicitly asks for an integration test.

