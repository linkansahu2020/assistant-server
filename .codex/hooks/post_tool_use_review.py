from _common import emit_json, is_project_mutation_command, read_payload


payload = read_payload()
command = payload.get("tool_input", {}).get("command", "")

if is_project_mutation_command(command):
    emit_json(
        {
            "systemMessage": "Project-affecting shell command ran. Re-check lint, tests, and build before finishing.",
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": "For this NestJS backend, prefer validating changes with `npm run lint`, `npm run test`, and `npm run build` after shell-driven edits or dependency changes."
            }
        }
    )
