from _common import emit_json, is_project_mutation_command, read_payload


payload = read_payload()
command = payload.get("tool_input", {}).get("command", "")

if is_project_mutation_command(command):
    emit_json(
        {
            "systemMessage": "Project-affecting shell command ran. Re-check ESLint and TypeScript before finishing.",
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": "For this NestJS backend, after Codex-driven code changes, run `npm run lint` and `npm run typecheck`. Run tests and build when the change scope warrants them."
            }
        }
    )
