from __future__ import annotations

import hashlib
import re
import time
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html import unescape
from typing import Any, Iterable
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from rfx1427.models import FetchResult, FetchStatus, NewsItem, utc_now


USER_AGENT = "rfx1427-finance/4.7 (news research; contact repository owner)"


# v4.7 staged fetch constants — WAJIB 7 target 10, early-stop 50→70→100.
# Python fetches; AI judges pool and decides early-stop.
STAGE_1_LIMIT = 50  # Stage 1: 1→50
STAGE_2_LIMIT = 70  # Stage 2: 51→70 (early-stop checkpoint if pool 7–10)
STAGE_3_LIMIT = 100  # Stage 3: 71→100 (final; 8/9 also stop)
POOL_MIN = 7       # WAJIB 7
POOL_TARGET = 10   # target 10 (output 7–10)


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

    def fetch(self, *, market: str, limit: int = 100) -> FetchResult:
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


def _rss_text(node: Any, names: tuple[str, ...]) -> str:
    """Return the joined text of the first child tag among ``names`` (or '')."""
    for name in names:
        child = node.find(name)
        if child is not None:
            return child.get_text(" ", strip=True)
    return ""


def parse_rss(body: str, source: str, page_url: str) -> list[NewsItem]:
    # Prefer lxml when available (fast, robust). Fall back to html.parser so a
    # missing XML tree-builder never crashes the feed — it degrades gracefully
    # to the same item-extraction logic below.
    try:
        soup = BeautifulSoup(body, "xml")
    except Exception:
        soup = BeautifulSoup(body, "html.parser")
    out: list[NewsItem] = []
    for node in soup.find_all(["item", "entry"]):
        link = node.find("link")
        url = (link.get("href") if link and link.has_attr("href") else link.get_text(" ", strip=True) if link else "")
        item = make_item(
            _rss_text(node, ("title", "headline")),
            _rss_text(node, ("description", "summary", "content")),
            urljoin(page_url, url), source,
            _rss_text(node, ("pubDate", "published", "updated")),
        )
        if item:
            out.append(item)
    return out


_ARTICLE_SELECTORS = ("article", "[data-test='article']", ".news-item", ".articleItem")
# Generik containers dipakai hanya sebagai fallback — hasilnya tetap di-filter.
_GENERIC_SELECTORS = ("[data-testid*='story']", ".post", ".feed__item", "div.card")


def _looks_like_navigation(title: str, url: str, page_url: str) -> bool:
    """Reject short nav/menu entries masquerading as news items."""
    if len(title) < 15:
        return True
    t = title.lower()
    if any(w in t for w in ("login", "sign up", "sign in", "sitemap", "newsletter", "subscribe", "contact us",
                            "search", "log in", "privacy", "terms of use", "all rights reserved", "cookie")):
        return True
    try:
        path = urlparse(url).path.rstrip("/")
    except ValueError:
        return True
    if not path:  # bare site root / www.example.com
        return True
    try:
        if urlparse(url).netloc == urlparse(page_url).netloc and path.count("/") <= 1:
            return True  # same-site short page like /about or /faq
    except ValueError:
        return True
    return False


def _parse_finviz_table(soup: BeautifulSoup, source: str, page_url: str) -> list[NewsItem]:
    """Finviz uses <tr class=\"news_table-row\"> with <a class=\"nn-tab-link\">, not <article>."""
    out: list[NewsItem] = []
    for row in soup.select("tr.news_table-row"):
        anchor = row.select_one("a.nn-tab-link[href]") or row.find("a", href=True)
        if not anchor:
            continue
        title = clean(anchor.get_text(" "))
        href = str(anchor.get("href", "")).strip()
        if not title or not href:
            continue
        url = urljoin(page_url, href)
        if _looks_like_navigation(title, url, page_url):
            continue
        # Finviz time is in td.news_date-cell ("09:27PM"); summary in data-boxover-text
        time_text: str | None = None
        time_cell = row.select_one("td.news_date-cell")
        if time_cell:
            time_text = clean(time_cell.get_text(" "))
        link_cell = row.select_one("td.news_link-cell")
        summary = clean(link_cell.get("data-boxover-text", "")) if link_cell and link_cell.has_attr("data-boxover-text") else ""
        if not summary:
            summary = title
        # pass raw time_text; parse_date will try, else stored as None and sorted last — still a valid item
        item = make_item(title, summary, url, source, time_text)
        if item:
            out.append(item)
    return out


def parse_html(body: str, source: str, page_url: str) -> list[NewsItem]:
    soup = BeautifulSoup(body, "html.parser")
    # Fast-path for Finviz table layout — must run before the generic article selectors
    if "finviz.com" in page_url:
        finviz_items = _parse_finviz_table(soup, source, page_url)
        if finviz_items:
            return finviz_items
    out: list[NewsItem] = []
    nodes: list[Any] = []
    for selector in (*_ARTICLE_SELECTORS, *_GENERIC_SELECTORS):
        nodes = soup.select(selector)
        if nodes:
            break
    for node in nodes:
        anchor = node.find("a", href=True)
        title_node = node.find(["h1", "h2", "h3", "h4"]) or anchor
        if not title_node or not anchor:
            continue
        title = clean(title_node.get_text(" "))
        if _looks_like_navigation(title, str(anchor["href"]), page_url):
            continue
        time_node = node.find("time")
        summary_node = node.find(["p", "div"], class_=re.compile("summary|description|excerpt", re.I))
        item = make_item(title, clean(summary_node.get_text(" ") if summary_node else node.get_text(" ")),
                         urljoin(page_url, anchor["href"]), source,
                         time_node.get("datetime") if time_node else None)
        if item:
            out.append(item)
    return out


def normalize_items(items: Iterable[NewsItem], limit: int = 100) -> list[NewsItem]:
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
