from __future__ import annotations

import re

from playwright.sync_api import sync_playwright

from providers.base import BaseProvider, ScrapeError

_COUNT_PATTERN = re.compile(r"-\s*(\d[\d.]*)\s*$")
_COUNT_SELECTOR = "[class*=count]"
_NAV_TIMEOUT = 30_000
_WAIT_TIMEOUT = 15_000


class IndexProvider(BaseProvider):
    """Headless-browser scraper for Index Oglasi (JavaScript-rendered SPA)."""

    def fetch_count(self, url: str) -> int:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            try:
                page = browser.new_page()
                page.goto(url, wait_until="networkidle", timeout=_NAV_TIMEOUT)
                page.wait_for_selector(_COUNT_SELECTOR, timeout=_WAIT_TIMEOUT)
                el = page.query_selector(_COUNT_SELECTOR)
                text = el.inner_text().strip() if el else ""
            finally:
                browser.close()

        if not text:
            raise ScrapeError(f"Count element not found on {url}")

        match = _COUNT_PATTERN.search(text)
        if match is None:
            raise ScrapeError(
                f"Cannot extract count from '{text}' on {url}"
            )

        digits = match.group(1).replace(".", "")
        try:
            return int(digits)
        except ValueError as exc:
            raise ScrapeError(f"Cannot parse count '{match.group(1)}' as int") from exc
