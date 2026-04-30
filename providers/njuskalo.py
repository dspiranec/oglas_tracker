from __future__ import annotations

import random

import requests
from bs4 import BeautifulSoup

from providers.base import BaseProvider, ScrapeError

_REQUEST_TIMEOUT = 15
_SELECTOR = "strong.entities-count"

_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.5; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
]

_BASE_HEADERS = {
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


def _random_headers() -> dict[str, str]:
    return {**_BASE_HEADERS, "User-Agent": random.choice(_USER_AGENTS)}


class NjuskaloProvider(BaseProvider):
    """Server-side HTML scraper for Njuškalo."""

    def fetch_count(self, url: str) -> int:
        response = requests.get(
            url,
            headers=_random_headers(),
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
