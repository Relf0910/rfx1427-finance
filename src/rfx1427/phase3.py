from __future__ import annotations

import argparse
import json
import re
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Iterable

import requests

NOT_AVAILABLE = "NOT AVAILABLE"
FORMS = ("10-K", "10-Q", "8-K", "6-K", "4")


@dataclass(slots=True)
class FilingFact:
    key: str
    value: Any = NOT_AVAILABLE
    unit: str = NOT_AVAILABLE
    form: str = NOT_AVAILABLE
    filing_date: str = NOT_AVAILABLE
    period: str = NOT_AVAILABLE
    accession_number: str = NOT_AVAILABLE
    source_url: str = NOT_AVAILABLE
    raw_fact_label: str = NOT_AVAILABLE

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class SecResult:
    ticker: str
    company: str = NOT_AVAILABLE
    cik: str = NOT_AVAILABLE
    sec_status: str = "UNVERIFIED"
    access_time: str = ""
    filings: list[dict[str, Any]] = field(default_factory=list)
    insider_transactions: list[dict[str, Any]] = field(default_factory=list)
    material_events: list[dict[str, Any]] = field(default_factory=list)
    collection_method: str = "python"
    error_code: str | None = None
    error_detail: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class SecAccessError(RuntimeError):
    def __init__(self, code: str, detail: str = "") -> None:
        self.code, self.detail = code, detail
        super().__init__(f"{code}: {detail}".strip())


class SecClient:
    """Official SEC EDGAR client. It fetches/parses only; AI owns verification labels."""

    def __init__(self, user_agent: str, timeout: tuple[int, int] = (5, 20), min_interval: float = 0.12) -> None:
        if not user_agent or "@" not in user_agent:
            raise ValueError("SEC_USER_AGENT must identify an application and contact email")
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": user_agent, "Accept-Encoding": "gzip, deflate"})
        self.timeout = timeout
        self.min_interval = min_interval
        self._last_request = 0.0
        self._ticker_map: dict[str, dict[str, Any]] | None = None

    def _get_json(self, url: str) -> dict[str, Any]:
        wait = self.min_interval - (time.monotonic() - self._last_request)
        if wait > 0:
            time.sleep(wait)
        try:
            response = self.session.get(url, timeout=self.timeout)
            self._last_request = time.monotonic()
            if response.status_code in {403, 429}:
                raise SecAccessError(f"HTTP_{response.status_code}", url)
            response.raise_for_status()
            payload = response.json()
            if not isinstance(payload, dict):
                raise SecAccessError("INVALID_JSON", url)
            return payload
        except SecAccessError:
            raise
        except (requests.RequestException, ValueError) as exc:
            raise SecAccessError("REQUEST_ERROR", str(exc)) from exc

    def ticker_map(self) -> dict[str, dict[str, Any]]:
        if self._ticker_map is None:
            payload = self._get_json("https://www.sec.gov/files/company_tickers.json")
            self._ticker_map = {}
            for row in payload.values():
                ticker = str(row.get("ticker", "")).upper()
                if ticker:
                    self._ticker_map[ticker] = {"cik": f"{int(row['cik_str']):010d}", "company": row.get("title", NOT_AVAILABLE)}
        return self._ticker_map

    def resolve(self, ticker: str) -> tuple[str, str]:
        row = self.ticker_map().get(ticker.upper().strip())
        if not row:
            raise SecAccessError("CIK_NOT_FOUND", ticker)
        return row["cik"], row["company"]

    def submissions(self, cik: str) -> dict[str, Any]:
        return self._get_json(f"https://data.sec.gov/submissions/CIK{cik}.json")

    def companyfacts(self, cik: str) -> dict[str, Any]:
        return self._get_json(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json")

    @staticmethod
    def _recent_filings(submissions: dict[str, Any]) -> list[dict[str, Any]]:
        recent = submissions.get("filings", {}).get("recent", {})
        rows: list[dict[str, Any]] = []
        size = len(recent.get("form", []))
        for i in range(size):
            form = recent["form"][i]
            if form in FORMS:
                rows.append({k: recent.get(k, [NOT_AVAILABLE] * size)[i] for k in (
                    "form", "filingDate", "reportDate", "accessionNumber", "primaryDocument")})
        return rows

    @staticmethod
    def _accession_matches(row_accn: Any, target: str) -> bool:
        """Match an XBRL accession against a submission accession regardless of dash format."""
        if not row_accn or not target:
            return False
        return str(row_accn) == target or str(row_accn).replace("-", "") == target.replace("-", "")

    @staticmethod
    def _concept(facts: dict[str, Any], names: tuple[str, ...], forms: tuple[str, ...], accn: str) -> FilingFact:
        """Return the fact value that belongs to the given accession, not the latest global one.

        Each filing must carry its own numbers; pulling the last matching value from the
        global facts history mixes periods across filings, so a non-match yields NOT AVAILABLE.
        """
        usgaap = facts.get("facts", {}).get("us-gaap", {})
        for name in names:
            concept = usgaap.get(name)
            if not concept:
                continue
            units = concept.get("units", {})
            for unit, values in units.items():
                for row in values:
                    if row.get("form") in forms and SecClient._accession_matches(row.get("accn"), accn):
                        return FilingFact(name, row.get("val", NOT_AVAILABLE), unit, row.get("form", NOT_AVAILABLE),
                                          row.get("filed", NOT_AVAILABLE), row.get("end", NOT_AVAILABLE),
                                          row.get("accn", NOT_AVAILABLE), NOT_AVAILABLE, name)
        return FilingFact(names[0], raw_fact_label=names[0])

    def fetch(self, ticker: str) -> SecResult:
        result = SecResult(ticker=ticker.upper().strip(), access_time=utc_now())
        try:
            cik, company = self.resolve(result.ticker)
            result.cik, result.company = cik, company
            submissions = self.submissions(cik)
            facts = self.companyfacts(cik)
            rows = self._recent_filings(submissions)
            for row in rows[:20]:
                accession = row["accessionNumber"].replace("-", "")
                document = row["primaryDocument"]
                source_url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accession}/{document}"
                filing = {"form": row["form"], "filing_date": row["filingDate"], "period": row["reportDate"],
                          "accession_number": row["accessionNumber"], "source_url": source_url,
                          "facts": {}}
                if row["form"] in {"10-K", "10-Q", "6-K"}:
                    forms = ("10-K", "10-Q", "6-K")
                    filing["facts"] = {"revenue": self._concept(facts, ("RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues"), forms, row["accessionNumber"]).to_dict(),
                                       "net_income_eps": self._concept(facts, ("EarningsPerShareDiluted", "ProfitLoss"), forms, row["accessionNumber"]).to_dict(),
                                       "total_debt": self._concept(facts, ("LongTermDebtAndFinanceLeaseObligationsCurrent", "LongTermDebtNoncurrent"), forms, row["accessionNumber"]).to_dict(),
                                       "cash_flow": self._concept(facts, ("NetCashProvidedByUsedInOperatingActivities",), forms, row["accessionNumber"]).to_dict(),
                                       "outstanding_shares": self._concept(facts, ("EntityCommonStockSharesOutstanding",), forms, row["accessionNumber"]).to_dict()}
                result.filings.append(filing)
                if row["form"] == "8-K":
                    result.material_events.append({"form": "8-K", "filing_date": row["filingDate"], "period": row["reportDate"], "source_url": source_url})
                if row["form"] == "4":
                    result.insider_transactions.append({"form": "4", "filing_date": row["filingDate"], "source_url": source_url})
            if not result.filings:
                raise SecAccessError("NO_RELEVANT_FILINGS", result.ticker)
            result.sec_status = "SUCCESS"
            return result
        except SecAccessError as exc:
            result.error_code, result.error_detail = exc.code, exc.detail
            return result


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def fetch_with_fallback(ticker: str, user_agent: str) -> SecResult:
    primary = SecClient(user_agent)
    result = primary.fetch(ticker)
    if result.sec_status == "SUCCESS":
        return result
    # Alternate remains official SEC: submissions endpoint via www.sec.gov with the same CIK.
    # A result that cannot be re-resolved remains explicitly UNVERIFIED; no web-search fallback.
    alternate = SecClient(user_agent, min_interval=0.2)
    try:
        cik, company = alternate.resolve(ticker)
        alt = alternate.submissions(cik)
        if alt.get("filings", {}).get("recent"):
            result.company, result.cik = company, cik
            result.collection_method = "python_sec_alternate"
            result.error_detail = f"primary={result.error_code}; alternate_available_but_parse_failed"
    except SecAccessError as exc:
        result.error_detail = f"primary={result.error_code}; alternate={exc.code}"
    result.sec_status = "UNVERIFIED"
    return result


def run_phase3(tickers: Iterable[str], user_agent: str) -> list[SecResult]:
    return [fetch_with_fallback(ticker, user_agent) for ticker in tickers if ticker.strip()]


def emit_jsonl(results: Iterable[SecResult], *, stream=sys.stdout) -> None:
    for result in results:
        print(json.dumps({"type": "phase3_sec_data", **result.to_dict()}, ensure_ascii=False), file=stream)


def main() -> int:
    parser = argparse.ArgumentParser(description="RFX1427 Finance Phase 3 SEC EDGAR fetcher")
    parser.add_argument("--tickers", nargs="+", required=True)
    parser.add_argument("--user-agent", required=True, help="Application name and contact email")
    args = parser.parse_args()
    results = run_phase3(args.tickers, args.user_agent)
    emit_jsonl(results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
