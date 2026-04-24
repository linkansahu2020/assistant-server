from _common import emit_json, is_destructive_command, is_project_validation_command, read_payload


payload = read_payload()
command = payload.get("tool_input", {}).get("command", "")

if is_destructive_command(command):
    emit_json(
        {
            "hookSpecificOutput": {
                "hookEventName": "PermissionRequest",
                "decision": {
                    "behavior": "deny",
                    "message": "Blocked destructive command by repository hook policy."
                }
            }
        }
    )
elif is_project_validation_command(command):
    emit_json(
        {
            "hookSpecificOutput": {
                "hookEventName": "PermissionRequest",
                "decision": {
                    "behavior": "allow"
                }
            }
        }
    )
