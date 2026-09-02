from __future__ import annotations

import json
from datetime import datetime, timezone

from rfx1427.models import FetchStatus, NewsItem
from rfx1427.phase1 import emit_jsonl, run_phase1
from rfx1427.sources.base import normalize_items
from rfx1427.sources.registry import build_adapter, supported_sources


def item(title: str, url: str, timestamp: str | None = None) -> NewsItem:
    return NewsItem(title.lower().replace(" ", "-"), title, "summary", url, "Test", timestamp, "summary")


def test_normalize_deduplicates_and_sorts():
    result = normalize_items([
        item("Older", "https://x/1", "2026-01-01T00:00:00+00:00"),
        item("Older", "https://x/1", "2026-01-01T00:00:00+00:00"),
        item("Newer", "https://x/2", "2026-01-02T00:00:00+00:00"),
    ])
    assert [x.title for x in result] == ["Newer", "Older"]


def test_all_listed_sources_have_adapters():
    assert len(supported_sources()) == 10
    for source in supported_sources():
        adapter = build_adapter(source)
        assert adapter.name


def test_custom_url_adapter():
    adapter = build_adapter("https://example.com/news")
    assert adapter.name == "custom"


def test_fetch_failure_is_explicit(monkeypatch):
    adapter = build_adapter("Investing.com")
    def fail(*args, **kwargs):
        from rfx1427.sources.base import SourceError
        raise SourceError("HTTP_403", "blocked")
    monkeypatch.setattr(adapter, "_get", fail)
    result = adapter.fetch(market="US")
    assert result.status == FetchStatus.FALLBACK_NEEDED.value
    assert result.error_code == "HTTP_403"


def test_jsonl_contract():
    result = run_phase1("not-a-real-source")
    lines = []
    import io
    stream = io.StringIO()
    emit_jsonl(result, stream=stream)
    lines = [json.loads(line) for line in stream.getvalue().splitlines()]
    assert lines[0]["type"] == "fetch_metadata"
    assert lines[0]["status"] == FetchStatus.FALLBACK_NEEDED.value
    assert lines[-1]["type"] == "fallback_signal"
