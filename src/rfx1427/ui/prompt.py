"""Interactive prompt helpers that adapt to the platform.

Usage::

    from rfx1427.ui import choose_one

    language = choose_one(
        "Pilih bahasa:",
        ["English", "Bahasa Melayu", "Other"],
        default="English",
    )
"""

from __future__ import annotations

import sys
from typing import Sequence

from rfx1427.ui.platform import detect_platform, is_interactive, supports_rich


def _fallback_select(prompt_text_str: str, options: Sequence[str], default: str | None) -> str:
    """Numbered-text fallback when rich or TTY is not available."""
    print(f"\n{prompt_text_str}")
    for idx, option in enumerate(options, start=1):
        marker = " (default)" if option == default else ""
        print(f"  {idx:>2}. {option}{marker}")

    while True:
        raw = input("> ").strip()
        if not raw and default is not None:
            return default
        try:
            choice = int(raw)
            if 1 <= choice <= len(options):
                return options[choice - 1]
            print(f"  Sila masukkan angka 1-{len(options)}.")
        except ValueError:
            # Allow direct text match.
            if raw in options:
                return raw
            print("  Pilihan tidak dikenali, cuba lagi.")
    return resolved_default  # pragma: no cover — unreachable but keeps linters quiet


def _rich_select(prompt_text_str: str, options: Sequence[str], default: str | None) -> str:
    """Arrow-key selector using rich."""
    try:
        from rich.console import Console
        from rich.prompt import Confirm, Prompt
    except ImportError:
        return _fallback_select(prompt_text_str, options, default)

    console = Console(stderr=True)
    try:
        from rich.prompt import Confirm
    except ImportError:
        return _fallback_select(prompt_text_str, options, default)

    # Use rich's built-in Prompt with choices when available (>=13.2).
    try:
        from rich.prompt import Prompt

        console.print(f"\n[bold]{prompt_text_str}[/bold]")
        formatted = [f"[cyan]{i+1}.[/cyan] {opt}" for i, opt in enumerate(options)]
        for line in formatted:
            console.print(line)

        value = Prompt.ask(
            "  Pilihan",
            default=default or options[0],
            console=console,
        )
        if value in options:
            return value
        return _fallback_select(prompt_text_str, options, default)
    except Exception:
        return _fallback_select(prompt_text_str, options, default)


def choose_one(
    prompt_text: str,
    options: Sequence[str],
    default: str | None = None,
) -> str:
    """Let the user pick one option.

    - Arrow-key menu via ``rich`` when a rich-capable terminal is
      detected.
    - Numbered text menu otherwise so every platform works.

    Parameters
    ----------
    prompt_text:
        Question shown to the user (e.g. ``"Pilih bahasa:"``).
    options:
        Ordered list of valid choices.
    default:
        Choice selected when the user presses Enter without input.
        Defaults to the first item in ``options`` when omitted.

    Returns
    -------
    str
        The chosen option string.
    """
    if not options:
        raise ValueError("options must not be empty")
    resolved_default = default if default is not None else options[0]
    if not supports_rich():
        return _fallback_select(prompt_text, options, resolved_default)
    return _rich_select(prompt_text, options, resolved_default)


def choose_multiple(
    prompt_text: str,
    options: Sequence[str],
    *,
    min: int = 1,
    default: list[str] | None = None,
) -> list[str]:
    """Let the user pick *any* number of options (comma-separated in
    fallback mode).

    Parameters
    ----------
    prompt_text:
        Question shown to the user.
    options:
        Choices the user may select.
    min:
        Minimum number of selections required.
    default:
        Pre-selected choices shown when the user presses Enter.

    Returns
    -------
    list[str]
        The selected option strings, guaranteed to have ``len() >= min``.
    """
    if not options:
        raise ValueError("options must not be empty")
    if min < 1:
        raise ValueError("min must be >= 1")
    resolved_default = default if default is not None else [options[0]]

    if not supports_rich():
        print(f"\n{prompt_text}")
        for idx, option in enumerate(options, start=1):
            marker = " (default)" if option in resolved_default else ""
            print(f"  {idx:>2}. {option}{marker}")
        selected: list[str] = []
        while len(selected) < min:
            raw = input("> Masukkan nombor pilihan (pisah dengan koma): ").strip()
            if not raw and default is not None:
                return list(default)
            indices = [x.strip() for x in raw.split(",") if x.strip()]
            try:
                chosen = [options[int(i) - 1] for i in indices if 1 <= int(i) <= len(options)]
            except (ValueError, IndexError):
                chosen = []
            if not chosen:
                print(f"  Masukkan nombor 1-{len(options)} yang sah.")
                continue
            for item in chosen:
                if item not in selected:
                    selected.append(item)
        return selected

    # Rich-capable path: reuse choose_one repeatedly (simplest safe path).
    selected: list[str] = []
    print(f"\n[bold]{prompt_text}[/bold]")
    while len(selected) < min:
        option = _rich_select("", options, options[0] if not selected else None)
        if option and option not in selected:
            selected.append(option)
    return selected


def prompt_text(prompt_text: str, default: str | None = None) -> str:
    """Free-form text prompt with an optional default."""
    if not is_interactive():
        val = input(f"{prompt_text} ").strip()
        return val or default or ""
    try:
        return input(f"{prompt_text} ").strip() or default or ""
    except EOFError:
        return default or ""
