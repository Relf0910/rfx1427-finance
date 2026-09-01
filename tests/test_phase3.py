from __future__ import annotations

import io
import json

from rfx1427.phase3 import FilingFact, SecAccessError, SecClient, SecResult, emit_jsonl, fetch_with_fallback


def test_cik_resolution_and_recent_filings():
    client = SecClient("RFX1427-Test test@example.com")
    client._ticker_map = {"AAPL": {"cik": "0000320193", "company": "Apple Inc."}}
    assert client.resolve("AAPL") == ("0000320193", "Apple Inc.")
    rows = client._recent_filings({"filings": {"recent": {"form": ["10-Q", "3"], "filingDate": ["2026-01-01", "2026-01-02"], "reportDate": ["2025-12-31", ""], "accessionNumber": ["1", "2"], "primaryDocument": ["a.htm", "b.htm"]}}})
    assert len(rows) == 1
    assert rows[0]["form"] == "10-Q"


def test_company_concept_prefers_supported_form():
    client = SecClient("RFX1427-Test test@example.com")
    facts = {"facts": {"us-gaap": {"Revenues": {"units": {"USD": [{"val": 1, "form": "10-Q", "filed": "2026-01-01", "end": "2025-12-31", "accn": "a"}]}}}}}
    fact = client._concept(facts, ("RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues"), ("10-K", "10-Q"))
    assert fact.value == 1
    assert fact.form == "10-Q"


def test_unknown_ticker_is_unverified(monkeypatch):
    client = SecClient("RFX1427-Test test@example.com")
    monkeypatch.setattr(client, "fetch", lambda ticker: SecResult(ticker=ticker, sec_status="UNVERIFIED", error_code="CIK_NOT_FOUND"))
    assert client.fetch("ZZZZ").sec_status == "UNVERIFIED"


def test_jsonl_contract():
    import io
    stream = io.StringIO()
    emit_jsonl([SecResult(ticker="AAPL", sec_status="UNVERIFIED")], stream=stream)
    payload = json.loads(stream.getvalue())
    assert payload["type"] == "phase3_sec_data"
    assert payload["sec_status"] == "UNVERIFIED"
