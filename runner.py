"""Running code blocks from notes in a separate process."""

import os
import shutil
import subprocess
import sys
import tempfile

DEFAULT_TIMEOUT = 10  # seconds


def _python_command() -> list[str] | None:
    # Inside a PyInstaller app, sys.executable is the app itself, not Python,
    # so look for a real Python on the PATH instead.
    if getattr(sys, "frozen", False):
        found = shutil.which("python3") or shutil.which("python")
        return [found] if found else None
    return [sys.executable]


def _racket_command() -> list[str] | None:
    found = shutil.which("racket")
    return [found] if found else None


def run_code(language: str, code: str, timeout: float = DEFAULT_TIMEOUT) -> str:
    """Run code and return everything it printed (stdout, then stderr).
    Never raises: problems come back as a message string."""
    language = language.lower()
    if language == "python":
        command, suffix = _python_command(), ".py"
    elif language == "racket":
        command, suffix = _racket_command(), ".rkt"
        if not code.lstrip().startswith("#lang"):
            code = "#lang racket\n" + code
    else:
        return f"Unsupported language: {language!r}. Use python or racket."

    if command is None:
        return f"Could not find {language} on this computer. Is it installed and on your PATH?"

    with tempfile.TemporaryDirectory() as folder:
        path = os.path.join(folder, "snippet" + suffix)
        with open(path, "w", encoding="utf-8") as f:
            f.write(code)
        try:
            result = subprocess.run(
                command + [path],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=folder,
            )
        except subprocess.TimeoutExpired:
            return f"Stopped: the code ran longer than {timeout:g} seconds."

    output = result.stdout + result.stderr
    if result.returncode != 0:
        output += f"\n(exited with code {result.returncode})"
    return output if output.strip() else "(no output)"
