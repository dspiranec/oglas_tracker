from __future__ import annotations

import re
import time

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

from providers.base import BaseProvider, ScrapeError

_PRIKAZANO_RE = re.compile(r"Prikazano\s+(\d+)\s+oglas", re.IGNORECASE)
_NAV_TIMEOUT = 60_000
_CF_POLL_INTERVAL = 3
_CF_MAX_WAIT = 30


class AvtonetProvider(BaseProvider):
    """Headless-browser scraper for Avto.net (Cloudflare-protected)."""

    def fetch_count(self, url: str) -> int:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(
                headless=True,
                args=["--disable-blink-features=AutomationControlled"],
            )
            try:
                context = browser.new_context(
                    user_agent=(
                        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                        "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
                    ),
                    locale="sl-SI",
                )
                page = context.new_page()
                page.goto(url, wait_until="domcontentloaded", timeout=_NAV_TIMEOUT)

                elapsed = 0
                while elapsed < _CF_MAX_WAIT:
                    body = page.inner_text("body")
                    if _PRIKAZANO_RE.search(body):
                        break
                    if "Just a moment" not in page.title():
                        break
                    time.sleep(_CF_POLL_INTERVAL)
                    elapsed += _CF_POLL_INTERVAL

                html = page.content()
            finally:
                browser.close()

        soup = BeautifulSoup(html, "html.parser")

        alert = soup.select_one("div.alert.alert-dark")
        if alert:
            match = _PRIKAZANO_RE.search(alert.get_text(strip=True))
            if match:
                return int(match.group(1))

        match = _PRIKAZANO_RE.search(soup.get_text())
        if match:
            return int(match.group(1))

        raise ScrapeError(f"'Prikazano N oglasov' pattern not found on {url}")
