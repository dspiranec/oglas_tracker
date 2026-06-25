from __future__ import annotations

import random
import re

import requests
from bs4 import BeautifulSoup

from providers.base import BaseProvider, ScrapeError

_REQUEST_TIMEOUT = 15
_COUNT_RE = re.compile(r"(\d+)\s+oglas", re.IGNORECASE)

_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
]

_BASE_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "hr-HR,hr;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}


def _random_headers() -> dict[str, str]:
    return {**_BASE_HEADERS, "User-Agent": random.choice(_USER_AGENTS)}


class BijeloJajeProvider(BaseProvider):
    """Server-side HTML scraper for Bijelo Jaje."""

    def fetch_count(self, url: str) -> int:
        response = requests.get(
            url,
            headers=_random_headers(),
            timeout=_REQUEST_TIMEOUT,
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()
        match = _COUNT_RE.search(text)
        if match is None:
            raise ScrapeError(
                f"Count pattern not found on {url}"
            )

        try:
            return int(match.group(1))
        except ValueError as exc:
            raise ScrapeError(f"Cannot parse count '{match.group(1)}' as int") from exc
