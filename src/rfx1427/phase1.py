from __future__ import annotations

import argparse
import json
import sys
from typing import Iterable

# Windows consoles often default to cp1252, which cannot encode the full
# UTF-8 text returned by news sources. Force UTF-8 so output never crashes.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from rfx1427.models import FetchResult, FetchStatus
from rfx1427.sources.registry import build_adapter, supported_sources


def run_phase1(source: str, market: str = "US", profile: str = "INTRADAY", limit: int = 50) -> FetchResult:
    """Fetch and normalize source items. AI remains responsible for all judgment."""
    try:
        adapter = build_adapter(source)
    except ValueError as exc:
        from rfx1427.models import utc_now
        return FetchResult(source, "unresolved", utc_now(), FetchStatus.FALLBACK_NEEDED.value,
                           error_code="UNSUPPORTED_SOURCE", error_detail=str(exc))
    result = adapter.fetch(market=market, limit=limit)
    return result


def emit_jsonl(result: FetchResult, *, stream=sys.stdout) -> None:
    print(json.dumps({"type": "fetch_metadata", **{k: v for k, v in result.to_dict().items() if k != "items"}}, ensure_ascii=False), file=stream)
    for item in result.items:
        print(json.dumps({"type": "news_item", **item.to_dict()}, ensure_ascii=False), file=stream)
    if result.status == FetchStatus.FALLBACK_NEEDED.value:
        print(json.dumps({"type": "fallback_signal", "status": result.status,
                          "reason": result.error_code, "detail": result.error_detail}, ensure_ascii=False), file=stream)


def main() -> int:
    parser = argparse.ArgumentParser(description="RFX1427 Finance Phase 1 Python fetcher")
    parser.add_argument("--source", required=True, help="Listed source name or custom URL")
    parser.add_argument("--market", default="US")
    parser.add_argument("--profile", default="INTRADAY", choices=["SCALPER", "INTRADAY", "SWING", "INVESTOR"])
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--list-sources", action="store_true")
    args = parser.parse_args()
    if args.list_sources:
        print("\n".join(supported_sources()))
        return 0
    result = run_phase1(args.source, args.market, args.profile, max(1, min(args.limit, 50)))
    emit_jsonl(result)
    return 0 if result.status == FetchStatus.SUCCESS.value else 2


if __name__ == "__main__":
    raise SystemExit(main())
