from _common import (
    emit_json,
    has_relevant_changes,
    message_mentions_required_validation,
    read_payload,
)


payload = read_payload()
last_message = payload.get("last_assistant_message")

if payload.get("stop_hook_active"):
    emit_json({"continue": True})
elif has_relevant_changes() and not message_mentions_required_validation(last_message):
    emit_json(
        {
            "decision": "block",
            "reason": "Before stopping after Codex changes, run `npm run lint` and `npm run typecheck`, or explicitly state why those checks could not be run."
        }
    )
else:
    emit_json({"continue": True})
