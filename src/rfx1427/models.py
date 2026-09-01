from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class FetchStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FALLBACK_NEEDED = "FALLBACK_NEEDED"
    BLOCKED = "BLOCKED"


@dataclass(slots=True)
class NewsItem:
    id: str
    title: str
    summary: str
    url: str
    source: str
    timestamp: str | None
    raw_text: str
    collection_method: str = "python"
    status: str = FetchStatus.SUCCESS.value

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class FetchResult:
    source_requested: str
    adapter_used: str
    access_time: str
    status: str
    items: list[NewsItem] = field(default_factory=list)
    items_fetched: int = 0
    items_after_dedup: int = 0
    fallback_used: bool = False
    error_code: str | None = None
    error_detail: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_requested": self.source_requested,
            "adapter_used": self.adapter_used,
            "access_time": self.access_time,
            "status": self.status,
            "items": [item.to_dict() for item in self.items],
            "items_fetched": self.items_fetched,
            "items_after_dedup": self.items_after_dedup,
            "fallback_used": self.fallback_used,
            "error_code": self.error_code,
            "error_detail": self.error_detail,
        }


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()
