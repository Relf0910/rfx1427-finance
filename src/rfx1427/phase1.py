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

from rfx1427.models import FetchResult, FetchStatus, utc_now
from rfx1427.sources.base import (
    POOL_MIN,
    POOL_TARGET,
    STAGE_1_LIMIT,
    STAGE_2_LIMIT,
    STAGE_3_LIMIT,
)
from rfx1427.sources.registry import build_adapter, supported_sources


# Market is locked to US (Gate 0 in v4.7.1).
SUPPORTED_MARKETS = ("US",)


def run_phase1(source: str, market: str = "US", profile: str = "INTRADAY", limit: int = 100) -> FetchResult:
    """Fetch and normalize source items. AI remains responsible for all judgment.

    v4.7.1: staged 50→70→100 with early-stop, WAJIB 7 target 10 (output 7–10).
    Python fetches in three stages; after each stage the pool is checked and
    fetching stops if the WAJIB threshold is already met:

      Stage 1: fetch 1→50. If pool ≥ POOL_MIN (7), continue to Stage 2 to reach POOL_TARGET (10).
      Stage 2: fetch 51→70. If pool has POOL_MIN..POOL_TARGET items at 70 → STOP early, skip 71→100.
      Stage 3: fetch 71→100. Only if pool < POOL_MIN at 70. If pool has 8/9 at 100 → STOP and output 8/9.

    The STAGE constants live in `sources/base.py`. Scan counts are never disclosed in output.

    Market is locked to US. Any value outside SUPPORTED_MARKETS returns FALLBACK_NEEDED
    with error_code="MARKET_NOT_SUPPORTED".
    """
    # Gate 0: market lock
    market_norm = (market or "US").upper().strip()
    if market_norm not in SUPPORTED_MARKETS:
        return FetchResult(source, "unresolved", utc_now(), FetchStatus.FALLBACK_NEEDED.value,
                           error_code="MARKET_NOT_SUPPORTED",
                           error_detail=f"market={market!r}; only US is supported in this build")

    try:
        adapter = build_adapter(source)
    except ValueError as exc:
        return FetchResult(source, "unresolved", utc_now(), FetchStatus.FALLBACK_NEEDED.value,
                           error_code="UNSUPPORTED_SOURCE", error_detail=str(exc))

    # Staged fetch: pull items in waves, stop when pool meets early-stop criteria.
    # Each call returns up to the stage limit; the pool handed to AI grows 50 → 70 → 100.
    #   Stage 1 (50):   if pool ≥ POOL_MIN (7), continue to Stage 2.
    #   Stage 2 (70):   if pool has POOL_MIN..POOL_TARGET (7..10) → STOP, skip Stage 3.
    #   Stage 3 (100):  only if pool < POOL_MIN at 70. If pool has 8/9 at 100 → STOP.
    pool = adapter.fetch(market=market_norm, limit=STAGE_1_LIMIT)
    if pool.status == FetchStatus.SUCCESS.value:
        if len(pool.items) < POOL_MIN:
            # Stage 2: pool still < 7, extend to 70
            pool = adapter.fetch(market=market_norm, limit=STAGE_2_LIMIT)
        if pool.status == FetchStatus.SUCCESS.value and POOL_MIN <= len(pool.items) <= POOL_TARGET:
            # Early stop: pool meets WAJIB 7 target 10 at 70, skip 71→100
            pass
        elif pool.status == FetchStatus.SUCCESS.value and len(pool.items) < POOL_MIN:
            # Stage 3: extend to 100 only if pool < 7 at 70
            pool = adapter.fetch(market=market_norm, limit=STAGE_3_LIMIT)
    # Hard cap at user's --limit
    if pool.status == FetchStatus.SUCCESS.value and limit < STAGE_3_LIMIT:
        pool.items = pool.items[:limit]
        pool.items_after_dedup = min(pool.items_after_dedup, limit)
    return pool


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
    parser.add_argument("--market", default="US", help="Market focus (Gate 0 locked to US)")
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
