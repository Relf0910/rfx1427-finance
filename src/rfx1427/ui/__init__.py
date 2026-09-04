"""Adaptive platform UI layer for rfx1427-finance.

Provides a single entry-point for interactive prompts that automatically
adapt to the host platform:

- Claude Code / VS Code terminals with ``rich`` installed → arrow-key
  selector menus (native-style choice UI).
- Any other environment (including plain stdin, OpenAI CLI, etc.) →
  numbered text fallback so the user can type their answer.

All high-level intake and configuration prompts in the framework route
through :func:`choose_one` and :func:`choose_multiple` in this module so
that the UI strategy is centralised and never duplicated.
"""

from rfx1427.ui.prompt import choose_one, choose_multiple, prompt_text
from rfx1427.ui.platform import detect_platform, is_interactive, supports_rich

__all__ = [
    "choose_one",
    "choose_multiple",
    "prompt_text",
    "detect_platform",
    "is_interactive",
    "supports_rich",
]
