from __future__ import annotations

import requests
from bs4 import BeautifulSoup

from providers.base import BaseProvider, ScrapeError

_REQUEST_TIMEOUT = 15
_SELECTOR = "strong.entities-count"
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "hr-HR,hr;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0",
}


class NjuskaloProvider(BaseProvider):
    """Server-side HTML scraper for Njuškalo."""

    def fetch_count(self, url: str) -> int:
        response = requests.get(
            url,
            headers=_HEADERS,
            timeout=_REQUEST_TIMEOUT,
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        tag = soup.select_one(_SELECTOR)
        if tag is None:
            raise ScrapeError(
                f"Selector '{_SELECTOR}' not found on {url}"
            )

        text = tag.get_text(strip=True).replace(".", "").replace(",", "")
        try:
            return int(text)
        except ValueError as exc:
            raise ScrapeError(f"Cannot parse count '{tag.get_text()}' as int") from exc
