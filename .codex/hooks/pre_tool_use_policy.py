from _common import emit_json, is_destructive_command, read_payload


payload = read_payload()
command = payload.get("tool_input", {}).get("command", "")

if is_destructive_command(command):
    emit_json(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": "Blocked destructive command by repository hook policy."
            }
        }
    )
