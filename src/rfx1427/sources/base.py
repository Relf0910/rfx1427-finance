from __future__ import annotations

import hashlib
import re
import time
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html import unescape
from typing import Iterable
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from rfx1427.models import FetchResult, FetchStatus, NewsItem, utc_now


USER_AGENT = "rfx1427-finance/4.5 (news research; contact repository owner)"


class SourceError(RuntimeError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(f"{code}: {detail}".strip())
        self.code = code
        self.detail = detail


class SourceAdapter(ABC):
    name = "base"

    def __init__(self, source_label: str) -> None:
        self.source_label = source_label
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": USER_AGENT,
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        })

    @abstractmethod
    def urls(self, market: str) -> list[str]:
        raise NotImplementedError

    def fetch(self, *, market: str, limit: int = 50) -> FetchResult:
        access_time = utc_now()
        try:
            items: list[NewsItem] = []
            for url in self.urls(market):
                body, content_type = self._get(url)
                items.extend(self.parse(body, url, content_type))
                if len(items) >= limit:
                    break
            items = normalize_items(items, limit)
            if not items:
                raise SourceError("EMPTY_RESPONSE", "no parseable news items")
            return FetchResult(self.source_label, self.name, access_time,
                               FetchStatus.SUCCESS.value, items, len(items), len(items))
        except SourceError as exc:
            return FetchResult(self.source_label, self.name, access_time,
                               FetchStatus.FALLBACK_NEEDED.value, error_code=exc.code,
                               error_detail=exc.detail)
        except requests.RequestException as exc:
            return FetchResult(self.source_label, self.name, access_time,
                               FetchStatus.FALLBACK_NEEDED.value, error_code="REQUEST_ERROR",
                               error_detail=str(exc))
        except Exception as exc:  # parser failures must become an explicit state
            return FetchResult(self.source_label, self.name, access_time,
                               FetchStatus.FALLBACK_NEEDED.value, error_code="PARSER_ERROR",
                               error_detail=str(exc))

    def _get(self, url: str) -> tuple[str, str]:
        last: requests.Response | None = None
        for attempt in range(2):
            response = self.session.get(url, timeout=(5, 20))
            last = response
            if response.status_code in {403, 429}:
                raise SourceError(f"HTTP_{response.status_code}", url)
            if response.ok:
                return response.text, response.headers.get("content-type", "")
            if response.status_code >= 500 and attempt == 0:
                time.sleep(0.5)
                continue
            response.raise_for_status()
        raise SourceError("HTTP_ERROR", f"{last.status_code if last else 'unknown'} {url}")

    def parse(self, body: str, page_url: str, content_type: str) -> list[NewsItem]:
        if "rss" in content_type or "xml" in content_type or "<rss" in body[:500].lower():
            return parse_rss(body, self.source_label, page_url)
        return parse_html(body, self.source_label, page_url)


def clean(value: str | None, max_chars: int = 500) -> str:
    text = unescape(re.sub(r"\s+", " ", value or "")).strip()
    return text[:max_chars]


def parse_date(value: str | None) -> str | None:
    if not value:
        return None
    try:
        return parsedate_to_datetime(value).astimezone(timezone.utc).isoformat()
    except (TypeError, ValueError, OverflowError):
        for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d %H:%M:%S"):
            try:
                dt = datetime.strptime(value.strip(), fmt)
                return dt.astimezone(timezone.utc).isoformat()
            except ValueError:
                pass
    return None


def make_item(title: str, summary: str, url: str, source: str,
              timestamp: str | None = None) -> NewsItem | None:
    title, summary, url = clean(title, 300), clean(summary, 700), clean(url, 1000)
    if not title or not url:
        return None
    raw = summary or title
    key = f"{title.lower()}|{url.lower()}".encode()
    return NewsItem(hashlib.sha256(key).hexdigest()[:16], title, summary, url, source,
                    parse_date(timestamp), clean(raw, 300))


def parse_rss(body: str, source: str, page_url: str) -> list[NewsItem]:
    soup = BeautifulSoup(body, "xml")
    out: list[NewsItem] = []
    for node in soup.find_all(["item", "entry"]):
        link = node.find("link")
        url = (link.get("href") if link and link.has_attr("href") else link.get_text(" ", strip=True) if link else "")
        item = make_item(
            node.find_text(["title", "headline"], default=""),
            node.find_text(["description", "summary", "content"], default=""),
            urljoin(page_url, url), source,
            node.find_text(["pubDate", "published", "updated"], default=""),
        )
        if item:
            out.append(item)
    return out


def parse_html(body: str, source: str, page_url: str) -> list[NewsItem]:
    soup = BeautifulSoup(body, "html.parser")
    out: list[NewsItem] = []
    selectors = ["article", "[data-test='article']", ".news-item", ".articleItem", "li"]
    nodes = []
    for selector in selectors:
        nodes = soup.select(selector)
        if nodes:
            break
    for node in nodes:
        anchor = node.find("a", href=True)
        title_node = node.find(["h1", "h2", "h3", "h4"]) or anchor
        if not title_node or not anchor:
            continue
        time_node = node.find("time")
        summary_node = node.find(["p", "div"], class_=re.compile("summary|description|excerpt", re.I))
        item = make_item(clean(title_node.get_text(" ")), clean(summary_node.get_text(" ") if summary_node else node.get_text(" ")),
                         urljoin(page_url, anchor["href"]), source,
                         time_node.get("datetime") if time_node else None)
        if item:
            out.append(item)
    return out


def normalize_items(items: Iterable[NewsItem], limit: int = 50) -> list[NewsItem]:
    seen: set[tuple[str, str]] = set()
    unique: list[NewsItem] = []
    for item in items:
        key = (re.sub(r"\W+", " ", item.title.lower()).strip(), item.url.lower())
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)
    unique.sort(key=lambda x: x.timestamp or "", reverse=True)
    return unique[:limit]
