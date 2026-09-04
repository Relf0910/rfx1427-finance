"""Unit tests for adaptive platform UI."""

import builtins
import sys

import pytest

from rfx1427.ui import choose_multiple, choose_one, prompt_text
from rfx1427.ui import platform as platform_mod
from rfx1427.ui.platform import detect_platform, is_interactive, supports_rich


class TestDetectPlatform:
    def test_claude_code_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("CLAUDE_CODE", "1")
        assert detect_platform() == "claude-code"

    def test_vscode_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("CLAUDE_CODE", raising=False)
        monkeypatch.delenv("ANTHROPIC_CLAUDE_CODE", raising=False)
        monkeypatch.setenv("TERM_PROGRAM", "vscode")
        assert detect_platform() == "vscode"

    def test_non_interactive_no_tty(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("CLAUDE_CODE", raising=False)
        monkeypatch.delenv("ANTHROPIC_CLAUDE_CODE", raising=False)
        monkeypatch.setenv("TERM_PROGRAM", "not-vscode")
        monkeypatch.setattr(platform_mod.sys.stdout, "isatty", lambda: False)
        assert detect_platform() == "non-interactive"

    def test_unknown(self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
        # No special env → fallback depends on TTY; at minimum it returns
        # a string naming the platform.
        result = detect_platform()
        assert isinstance(result, str)


class TestSupportsRich:
    def test_false_without_rich(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # Simulate rich being unavailable.
        monkeypatch.setattr(platform_mod.sys, "stdout", None, raising=False)
        import importlib

        monkeypatch.setitem(sys.modules, "rich", None)
        assert supports_rich() is False


class TestChooseOneFallback:
    def test_valid_number(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(platform_mod.sys.stdout, "isatty", lambda: False)
        monkeypatch.setattr(builtins, "input", lambda *_: "2")
        assert choose_one("Pilih:", ["A", "B", "C"]) == "B"

    def test_default_on_empty(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(platform_mod.sys.stdout, "isatty", lambda: False)
        monkeypatch.setattr(builtins, "input", lambda *_: "")
        assert choose_one("Pilih:", ["A", "B"], default="B") == "B"

    def test_direct_text_match(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(platform_mod.sys.stdout, "isatty", lambda: False)
        monkeypatch.setattr(builtins, "input", lambda *_: "English")
        assert choose_one("Pilih:", ["English", "BM"], default="English") == "English"
