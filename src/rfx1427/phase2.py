from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Iterable

import requests

NOT_AVAILABLE = "NOT AVAILABLE"


@dataclass(slots=True)
class MarketData:
    ticker: str
    company: str = NOT_AVAILABLE
    primary_tool: str = NOT_AVAILABLE
    fetch_status: str = "UNVERIFIED"
    access_time: str = ""
    price: float | str = NOT_AVAILABLE
    change_percent: float | str = NOT_AVAILABLE
    volume: int | str = NOT_AVAILABLE
    technical_levels: dict[str, float | str] = field(default_factory=dict)
    analyst_data: dict[str, Any] = field(default_factory=dict)
    earnings: dict[str, Any] = field(default_factory=dict)
    recent_news: list[dict[str, Any]] = field(default_factory=list)
    collection_method: str = "python"
    error_code: str | None = None
    error_detail: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class PrimaryToolError(RuntimeError):
    def __init__(self, code: str, detail: str = "") -> None:
        self.code, self.detail = code, detail
        super().__init__(f"{code}: {detail}".strip())


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _float(value: Any) -> float | str:
    try:
        if value is None or (isinstance(value, float) and math.isnan(value)):
            return NOT_AVAILABLE
        return float(value)
    except (TypeError, ValueError):
        return NOT_AVAILABLE


def _last(history: Any, column: str) -> float | str:
    try:
        if history is None or history.empty or column not in history:
            return NOT_AVAILABLE
        return _float(history[column].iloc[-1])
    except (IndexError, KeyError, AttributeError):
        return NOT_AVAILABLE


def _levels(profile: str, history: Any) -> dict[str, float | str]:
    profile = profile.upper()
    close = _last(history, "Close")
    levels: dict[str, float | str] = {}
    if profile == "SCALPER":
        levels = {"pre_market_high": NOT_AVAILABLE, "pre_market_low": NOT_AVAILABLE, "R1": NOT_AVAILABLE, "R2": NOT_AVAILABLE}
    elif profile == "INTRADAY":
        levels = {"VWAP": NOT_AVAILABLE, "opening_range_high": NOT_AVAILABLE, "opening_range_low": NOT_AVAILABLE}
        if history is not None and not getattr(history, "empty", True):
            high, low, volume = history.get("High"), history.get("Low"), history.get("Volume")
            try:
                levels["VWAP"] = _float(((high * volume).sum() + (low * volume).sum()) / (2 * volume.sum()))
            except (AttributeError, TypeError, ZeroDivisionError):
                pass
    elif profile == "SWING":
        levels = {"SMA_20": NOT_AVAILABLE, "SMA_50": NOT_AVAILABLE, "recent_swing_high": NOT_AVAILABLE, "recent_swing_low": NOT_AVAILABLE}
        try:
            closes = history["Close"]
            levels["SMA_20"] = _float(closes.tail(20).mean())
            levels["SMA_50"] = _float(closes.tail(50).mean())
            levels["recent_swing_high"] = _float(history["High"].tail(20).max())
            levels["recent_swing_low"] = _float(history["Low"].tail(20).min())
        except (AttributeError, KeyError, TypeError):
            pass
    elif profile == "INVESTOR":
        levels = {"52_week_high": NOT_AVAILABLE, "52_week_low": NOT_AVAILABLE, "current_PE": NOT_AVAILABLE, "historical_valuation": NOT_AVAILABLE}
        try:
            levels["52_week_high"] = _float(history["High"].tail(252).max())
            levels["52_week_low"] = _float(history["Low"].tail(252).min())
        except (AttributeError, KeyError, TypeError):
            pass
    return levels


class YFinanceAdapter:
    name = "yfinance"

    def fetch(self, ticker: str, profile: str) -> MarketData:
        try:
            import yfinance as yf
        except ImportError as exc:
            raise PrimaryToolError("DEPENDENCY_MISSING", "yfinance") from exc
        try:
            obj = yf.Ticker(ticker)
            history = obj.history(period="1y", auto_adjust=False)
            if history is None or history.empty:
                raise PrimaryToolError("EMPTY_RESPONSE", ticker)
            info = getattr(obj, "info", {}) or {}
            fast_info = getattr(obj, "fast_info", {}) or {}
            price = _last(history, "Close")
            previous = _float(history["Close"].iloc[-2]) if len(history) > 1 else NOT_AVAILABLE
            change = NOT_AVAILABLE
            if isinstance(price, float) and isinstance(previous, float) and previous:
                change = round((price - previous) / previous * 100, 4)
            return MarketData(ticker=ticker, primary_tool="Google Finance / Yahoo", fetch_status="SUCCESS", access_time=utc_now(),
                              company=info.get("longName", info.get("shortName", NOT_AVAILABLE)),
                              price=price, change_percent=change, volume=_last(history, "Volume"), technical_levels=_levels(profile, history),
                              analyst_data={"target": _float(info.get("targetMeanPrice")), "rating": info.get("recommendationKey", NOT_AVAILABLE)},
                              earnings={"next_earnings": info.get("earningsTimestamp", NOT_AVAILABLE)}, recent_news=[])
        except PrimaryToolError:
            raise
        except Exception as exc:
            raise PrimaryToolError("FETCH_ERROR", str(exc)) from exc


class FinvizAdapter:
    name = "finviz"

    def fetch(self, ticker: str, profile: str) -> MarketData:
        # Direct HTML scrape. The finvizfinance 0.14.x library hits a
        # "'NoneType' object has no attribute 'find_all'" bug because Finviz
        # changed their snapshot table structure. We re-implement the parse
        # here using requests + BeautifulSoup, both already in our deps.
        url = f"https://finviz.com/quote.ashx?t={ticker}"
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=(5, 20))
            if response.status_code in {403, 429}:
                raise PrimaryToolError(f"HTTP_{response.status_code}", url)
            response.raise_for_status()
        except requests.RequestException as exc:
            raise PrimaryToolError("REQUEST_ERROR", str(exc)) from exc
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")
            # Build {label: value} map by walking all snapshot-table cells.
            data: dict[str, str] = {}
            for cell in soup.select("td.snapshot-table2__cell, td.snapshot-table2__cell-s"):
                txt = cell.get_text(strip=True)
                if not txt:
                    continue
                # Cells come in label/value pairs, no class differentiation — collect raw.
                data.setdefault(f"_raw_{len(data)}", txt)
            # Better: iterate <tr> rows in any snapshot table and pair cells (label, value).
            data = {}
            for row in soup.select("tr"):
                cells = [c.get_text(strip=True) for c in row.select("td")]
                for i in range(0, len(cells) - 1, 2):
                    label, value = cells[i], cells[i + 1]
                    if label and value and label not in data:
                        data[label] = value
            if not data:
                raise PrimaryToolError("EMPTY_RESPONSE", ticker)
            company_tag = soup.select_one("h2.quote-header_ticker-wrapper__name")
            company = company_tag.get_text(strip=True) if company_tag else NOT_AVAILABLE
            levels = {
                "RSI": _float(data.get("RSI", "")),
                "SMA_20": _float(str(data.get("SMA20", "")).replace("%", "")),
                "SMA_50": _float(str(data.get("SMA50", "")).replace("%", "")),
                "52_week_high": _float(str(data.get("52W High", "")).split()[0]),
                "52_week_low": _float(str(data.get("52W Low", "")).split()[0]),
            }
            return MarketData(ticker=ticker, primary_tool="Finviz", fetch_status="SUCCESS", access_time=utc_now(),
                              company=company,
                              price=_float(data.get("Price")),
                              change_percent=_float(str(data.get("Change %", "")).replace("%", "")),
                              volume=data.get("Volume", NOT_AVAILABLE),
                              technical_levels=levels,
                              analyst_data={"target": _float(str(data.get("Target Price", "")).split()[0]),
                                            "rating": data.get("Recom", NOT_AVAILABLE)},
                              earnings={"EPS": data.get("EPS (ttm)", NOT_AVAILABLE),
                                        "revenue": data.get("Income", NOT_AVAILABLE),
                                        "next_earnings": data.get("Earnings", NOT_AVAILABLE)})
        except PrimaryToolError:
            raise
        except Exception as exc:
            raise PrimaryToolError("FETCH_ERROR", str(exc)) from exc


class MarketBeatAdapter:
    name = "marketbeat"

    def fetch(self, ticker: str, profile: str) -> MarketData:
        url = f"https://www.marketbeat.com/stocks/{ticker[:1].lower()}/{ticker.lower()}/"
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=(5, 20))
            if response.status_code in {403, 429}:
                raise PrimaryToolError(f"HTTP_{response.status_code}", url)
            response.raise_for_status()
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")
            text = " ".join(soup.stripped_strings)
            if not text:
                raise PrimaryToolError("EMPTY_RESPONSE", ticker)
            # MarketBeat's actual price/consensus figures are rendered by JavaScript,
            # so the static HTML carries only navigation text. Treating those menu
            # strings as data would fabricate a SUCCESS payload, so be honest instead.
            raise PrimaryToolError("NOT_DATA_IN_STATIC_HTML", url)
        except PrimaryToolError:
            raise
        except requests.RequestException as exc:
            raise PrimaryToolError("REQUEST_ERROR", str(exc)) from exc


ADAPTERS = {"yahoo": YFinanceAdapter(), "google finance": YFinanceAdapter(), "finviz": FinvizAdapter(), "marketbeat": MarketBeatAdapter()}


def _alternate(ticker: str, profile: str, primary_tool: str) -> MarketData:
    """Alternate method is deliberately conservative: yfinance only, never AI judgment."""
    if primary_tool.lower() in {"google finance", "yahoo"}:
        raise PrimaryToolError("NO_ALTERNATE_METHOD", "primary already uses yfinance")
    return YFinanceAdapter().fetch(ticker, profile)


def fetch_ticker(ticker: str, primary_tool: str, profile: str) -> MarketData:
    access_time = utc_now()
    adapter = ADAPTERS.get(primary_tool.strip().lower())
    if adapter is None:
        return MarketData(ticker=ticker, primary_tool=primary_tool, access_time=access_time, fetch_status="UNVERIFIED", error_code="UNSUPPORTED_TOOL")
    try:
        return adapter.fetch(ticker.strip().upper(), profile)
    except PrimaryToolError as first:
        try:
            result = _alternate(ticker.strip().upper(), profile, primary_tool)
            result.collection_method = "python_alternate"
            return result
        except PrimaryToolError as second:
            return MarketData(ticker=ticker.strip().upper(), primary_tool=primary_tool, access_time=access_time,
                              fetch_status="BLOCKED", error_code=second.code, error_detail=f"primary={first.code}; alternate={second.code}")


def run_phase2(opportunities: Iterable[dict[str, Any]], primary_tool: str, profile: str) -> list[MarketData]:
    return [fetch_ticker(str(row.get("ticker", "")), primary_tool, profile) for row in opportunities if row.get("ticker")]


def emit_jsonl(results: list[MarketData], *, stream=sys.stdout) -> None:
    for result in results:
        payload = {"type": "phase2_market_data", **result.to_dict()}
        print(json.dumps(payload, ensure_ascii=False), file=stream)


def main() -> int:
    parser = argparse.ArgumentParser(description="RFX1427 Finance Phase 2 Python market-data fetcher")
    parser.add_argument("--primary-tool", required=True, choices=["Google Finance", "Yahoo", "Finviz", "MarketBeat"])
    parser.add_argument("--profile", required=True, choices=["SCALPER", "INTRADAY", "SWING", "INVESTOR"])
    parser.add_argument("--opportunities", required=True, help="JSON file containing Phase 1 opportunity objects")
    args = parser.parse_args()
    with open(args.opportunities, encoding="utf-8") as handle:
        opportunities = json.load(handle)
    results = run_phase2(opportunities, args.primary_tool, args.profile)
    emit_jsonl(results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
