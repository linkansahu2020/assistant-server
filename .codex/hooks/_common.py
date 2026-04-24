import json
import re
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
RELEVANT_CHANGE_PATTERN = re.compile(
    r"(^src/|^test/|^package(-lock)?\.json$|^tsconfig(\..+)?\.json$|^nest-cli\.json$|^eslint\.config\.)"
)
VALIDATION_PATTERN = re.compile(r"\bnpm run (lint|test|build)\b|validation passed", re.IGNORECASE)


def read_payload():
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    return json.loads(raw)


def emit_json(payload):
    print(json.dumps(payload))


def run_git(*args):
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return result


def changed_files():
    result = run_git("status", "--porcelain")
    if result.returncode != 0:
        return []

    files = []
    for line in result.stdout.splitlines():
        if len(line) < 4:
            continue
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        files.append(path.strip())
    return files


def has_relevant_changes():
    return any(RELEVANT_CHANGE_PATTERN.search(path) for path in changed_files())


def message_mentions_validation(message):
    return bool(message and VALIDATION_PATTERN.search(message))


def is_destructive_command(command):
    patterns = [
        r"\brm\s+-rf\b",
        r"\bgit\s+reset\s+--hard\b",
        r"\bgit\s+clean\s+-f[dxf]*\b",
        r"\bgit\s+checkout\s+--\b",
        r"\bgit\s+branch\s+-D\b",
        r"\bmv\b.+\s+/dev/null\b",
    ]
    return any(re.search(pattern, command) for pattern in patterns)


def is_project_validation_command(command):
    safe_commands = [
        r"^\s*npm run lint\b",
        r"^\s*npm run test\b",
        r"^\s*npm run build\b",
        r"^\s*git status\b",
        r"^\s*git diff\b",
    ]
    return any(re.search(pattern, command) for pattern in safe_commands)


def is_project_mutation_command(command):
    mutation_patterns = [
        r"\bnpm\s+(install|uninstall|update|ci)\b",
        r"\bnpx\s+@nestjs/cli\b",
        r"\bgit\s+(merge|apply|am|cherry-pick)\b",
        r"\bcp\b",
        r"\bmv\b",
        r"\bsed\b",
    ]
    return any(re.search(pattern, command) for pattern in mutation_patterns)
