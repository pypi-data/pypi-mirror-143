from __future__ import annotations

import subprocess


def run(command: str, with_console: bool = True, line_limit: int | None = None) -> None:
    process = subprocess.run(command.split(), capture_output=True, text=True)
    print()
    if with_console:
        print("```console")
        print(f"$ {command}")

    output = process.stdout.strip()
    if line_limit:
        output = "".join(output.splitlines(keepends=True)[:line_limit]) + "..."
    print(output)

    if with_console:
        print("```")
    print()
