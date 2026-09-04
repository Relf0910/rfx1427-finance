"""Platform detection for adaptive UI.

The goal is to choose the friendliest prompt style automatically:

- Claude Code (env ``CLAUDE_CODE``) and most modern terminals can render
  arrow-key interactive selectors via ``rich``.  We treat those as
  *interactive-capable*.
- Environments that strip escape sequences or that never present a TTY
  (OpenAI CLI, CI runners, ``< /dev/null``) cannot do arrow menus and
  should use the numbered-text fallback so the flow never breaks.

``rich`` is *optional* — if it is not installed the selector falls back
to plain input whether or not the terminal is interactive.  This keeps
the dependency truly optional while still shipping the polished UI when
available.
"""

from __future__ import annotations

import os
import sys


# --- environment detection -------------------------------------------------

_CLAUDE_CODE_ENV = ("CLAUDE_CODE", "ANTHROPIC_CLAUDE_CODE")
_VSCODE_ENV = ("TERM_PROGRAM",)  # set to "vscode" by VS Code terminal


def _env_on(names: tuple[str, ...]) -> bool:
    """Return True if any of the given env vars is set to a truthy value."""
    for name in names:
        value = os.environ.get(name, "").strip()
        if value and value.lower() not in {"0", "false", "no"}:
            return True
    return False


# --- public helpers --------------------------------------------------------


def is_interactive() -> bool:
    """Return True when stdout *looks* like a real, interactive TTY."""
    return bool(sys.stdout.isatty())


def supports_rich() -> bool:
    """True when ``rich`` is importable *and* stdout is a TTY."""
    try:
        import rich  # noqa: F401
    except ImportError:
        return False
    return is_interactive()


def detect_platform() -> str:
    """Classify the host platform for UI selection.

    Returns one of:
        ``"claude-code"``  — running inside Claude Code
        ``"vscode"``       — running in a VS Code terminal
        ``"interactive"``  — TTY but not the special cases above
        ``"non-interactive"`` — piped / redirected stdin (fallback)
        ``"unknown"``      — everything else
    """
    # Prefer the explicit Claude Code flag.
    if any(os.environ.get(env) for env in _CLAUDE_CODE_ENV):
        return "claude-code"

    # VS Code internal terminal sets TERM_PROGRAM.
    if os.environ.get("TERM_PROGRAM", "").lower() in {"vscode"}:
        return "vscode"

    if is_interactive():
        return "interactive"

    # If stdin was redirected (``<`` / piped) the process is non-interactive
    # and we should fall back to text prompts.
    if not is_interactive():
        return "non-interactive"

    return "unknown"
