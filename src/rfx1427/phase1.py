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


def run_phase1(source: str, market: str = "US", profile: str = "INTRADAY", limit: int = 100) -> FetchResult:
    """Fetch and normalize source items. AI remains responsible for all judgment.

    v4.7: staged 50→70→100 with early-stop, WAJIB 7 target 10 (output 7–10).
    Python fetches up to limit (default 100); AI reads staged pool:
    1→50 (if ≥7 continue to 10), 51→70 (if pool 7–10 at 70 STOP), 71→100
    (if 8/9 at 100 STOP). STAGE_1=50, STAGE_2=70, STAGE_3=100, POOL_MIN=7,
    POOL_TARGET=10 defined in sources/base.py. Scan counts never disclosed.
    """
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
    parser.add_argument("--list-sources", action="store_true", help="List all supported source names and exit")
    parser.add_argument("--source", help="Listed source name or custom URL (required unless --list-sources)")
    parser.add_argument("--market", default="US")
    parser.add_argument("--profile", default="INTRADAY", choices=["SCALPER", "INTRADAY", "SWING", "INVESTOR"])
    parser.add_argument("--limit", type=int, default=100)
    args = parser.parse_args()
    if args.list_sources:
        print("\n".join(supported_sources()))
        return 0
    if not args.source:
        parser.error("the following arguments are required: --source (or pass --list-sources)")
    result = run_phase1(args.source, args.market, args.profile, max(1, min(args.limit, 100)))
    emit_jsonl(result)
    return 0 if result.status == FetchStatus.SUCCESS.value else 2


if __name__ == "__main__":
    raise SystemExit(main())
