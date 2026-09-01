from __future__ import annotations

import io
import json

import pandas as pd

from rfx1427.phase2 import MarketData, PrimaryToolError, _levels, emit_jsonl, fetch_ticker, run_phase2


def history():
    idx = pd.date_range("2026-01-01", periods=60, freq="D")
    return pd.DataFrame({
        "Open": range(100, 160),
        "High": range(101, 161),
        "Low": range(99, 159),
        "Close": range(100, 160),
        "Volume": [1000] * 60,
    }, index=idx)


def test_profile_levels():
    data = history()
    assert set(_levels("SCALPER", data)) == {"pre_market_high", "pre_market_low", "R1", "R2"}
    assert isinstance(_levels("INTRADAY", data)["VWAP"], float)
    assert isinstance(_levels("SWING", data)["SMA_20"], float)
    assert isinstance(_levels("INVESTOR", data)["52_week_high"], float)


def test_run_phase2_skips_missing_ticker():
    results = run_phase2([{"ticker": ""}, {"company": "Missing"}], "Finviz", "INTRADAY")
    assert results == []


def test_missing_primary_and_alternate_is_explicit(monkeypatch):
    from rfx1427 import phase2

    def fail(*args, **kwargs):
        raise PrimaryToolError("TEST_FAILURE", "forced")

    monkeypatch.setattr(phase2.ADAPTERS["finviz"], "fetch", fail)
    monkeypatch.setattr(phase2.YFinanceAdapter, "fetch", fail)
    result = fetch_ticker("AAPL", "Finviz", "INTRADAY")
    assert result.fetch_status == "BLOCKED"
    assert result.error_code == "TEST_FAILURE"


def test_jsonl_has_phase2_contract():
    stream = io.StringIO()
    emit_jsonl([MarketData(ticker="AAPL", primary_tool="Finviz", fetch_status="BLOCKED")], stream=stream)
    payload = json.loads(stream.getvalue())
    assert payload["type"] == "phase2_market_data"
    assert payload["fetch_status"] == "BLOCKED"
    assert payload["ticker"] == "AAPL"
