from __future__ import annotations

from urllib.parse import urlparse

from rfx1427.sources.base import SourceAdapter


SOURCE_URLS: dict[str, list[str]] = {
    "finviz": ["https://finviz.com/news.ashx"],
    "yahoo finance": ["https://finance.yahoo.com/topic/stock-market-news/"],
    "investing.com": ["https://www.investing.com/news/stock-market-news"],
    "tradingview": ["https://www.tradingview.com/markets/stocks-usa/market-movers-active/"],
    "stocktitan": ["https://www.stocktitan.net/news"],
    "pr newswire": ["https://www.prnewswire.com/news-releases/news-releases-list/"],
    "globenewswire": ["https://www.globenewswire.com/RssFeed/subjectcode/39"],
    "motley fool": ["https://www.fool.com/investing-news/"],
    "barchart": ["https://www.barchart.com/stocks/news"],
    "stockanalysis.com": ["https://stockanalysis.com/news/"],
}

ALIASES = {
    "yahoo": "yahoo finance",
    "yahoo finance": "yahoo finance",
    "investing": "investing.com",
    "investing.com": "investing.com",
    "pr newswire": "pr newswire",
    "prnewswire": "pr newswire",
    "globe newswire": "globenewswire",
    "globenewswire": "globenewswire",
    "motley fool": "motley fool",
    "stock analysis": "stockanalysis.com",
    "stockanalysis": "stockanalysis.com",
}


class ListedSourceAdapter(SourceAdapter):
    def __init__(self, source_key: str) -> None:
        self.source_key = source_key
        super().__init__(source_key.title() if source_key != "investing.com" else "Investing.com")
        self.name = source_key.replace(" ", "_").replace(".", "_")

    def urls(self, market: str) -> list[str]:
        return SOURCE_URLS[self.source_key]


class CustomSourceAdapter(SourceAdapter):
    name = "custom"

    def __init__(self, source: str) -> None:
        self.source = source
        super().__init__(source)

    def urls(self, market: str) -> list[str]:
        if not urlparse(self.source).scheme:
            raise ValueError("custom source must be a URL")
        return [self.source]


def build_adapter(source: str) -> SourceAdapter:
    raw = source.strip()
    key = ALIASES.get(raw.lower(), raw.lower())
    if key in SOURCE_URLS:
        return ListedSourceAdapter(key)
    if key.startswith(("http://", "https://")):
        return CustomSourceAdapter(raw)
    raise ValueError(f"unsupported source: {source}")


def supported_sources() -> tuple[str, ...]:
    return tuple(SOURCE_URLS)
