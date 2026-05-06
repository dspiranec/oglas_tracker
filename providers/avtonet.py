from __future__ import annotations

import re
import time

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

from providers.base import BaseProvider, ScrapeError

_PRIKAZANO_RE = re.compile(r"Prikazano\s+(\d+)\s+oglas", re.IGNORECASE)
_NAV_TIMEOUT = 60_000
_CF_POLL_INTERVAL = 3
_CF_MAX_WAIT = 45

_STEALTH_JS = """
Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
Object.defineProperty(navigator, 'languages', {get: () => ['sl-SI', 'sl', 'en']});
Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
window.chrome = {runtime: {}};
"""


class AvtonetProvider(BaseProvider):
    """Headless-browser scraper for Avto.net (Cloudflare-protected)."""

    def fetch_count(self, url: str) -> int:
        with sync_playwright() as pw:
            browser = pw.firefox.launch(headless=True)
            try:
                context = browser.new_context(
                    user_agent=(
                        "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) "
                        "Gecko/20100101 Firefox/128.0"
                    ),
                    locale="sl-SI",
                    viewport={"width": 1920, "height": 1080},
                )
                page = context.new_page()
                page.add_init_script(_STEALTH_JS)
                page.goto(url, wait_until="domcontentloaded", timeout=_NAV_TIMEOUT)

                elapsed = 0
                while elapsed < _CF_MAX_WAIT:
                    body = page.inner_text("body")
                    if _PRIKAZANO_RE.search(body):
                        break
                    title = page.title()
                    if "Just a moment" not in title and "Checking" not in title:
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
