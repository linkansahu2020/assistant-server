from _common import emit_json, read_payload


payload = read_payload()
prompt = payload.get("prompt", "")

message = (
    "This repository is a NestJS backend. Prefer TypeScript changes in `src/` and `test/`, "
    "use npm scripts for validation, keep Git work on `master`, and avoid destructive git or shell operations."
)

if "hook" in prompt.lower():
    message += " When editing Codex configuration, keep `.codex/config.toml` and `.codex/hooks.json` in sync."

emit_json(
    {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": message
        }
    }
)
