from __future__ import annotations

import re

from bs4 import BeautifulSoup
from curl_cffi import requests

from providers.base import BaseProvider, ScrapeError

_REQUEST_TIMEOUT = 20
_PRIKAZANO_RE = re.compile(r"Prikazano\s+(\d+)\s+oglas", re.IGNORECASE)


class AvtonetProvider(BaseProvider):
    """Scraper for Avto.net using curl_cffi to bypass Cloudflare."""

    def fetch_count(self, url: str) -> int:
        response = requests.get(url, impersonate="chrome", timeout=_REQUEST_TIMEOUT)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        alert = soup.select_one("div.alert.alert-dark")
        if alert:
            text = alert.get_text(strip=True)
            match = _PRIKAZANO_RE.search(text)
            if match:
                return int(match.group(1))

        match = _PRIKAZANO_RE.search(soup.get_text())
        if match:
            return int(match.group(1))

        raise ScrapeError(
            f"'Prikazano N oglasov' pattern not found on {url}"
        )
