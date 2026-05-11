from __future__ import annotations

import re

from playwright.sync_api import sync_playwright, Page

from providers.base import BaseProvider, ScrapeError, ScrapeResult

_COUNT_SELECTORS = [
    "[class*=count]",
    "[class*=Count]",
    "[class*=results]",
    "[class*=Results]",
]
_OGLASA_RE = re.compile(r"(\d[\d.]*)\s+oglas", re.IGNORECASE)
_NAV_TIMEOUT = 30_000
_WAIT_TIMEOUT = 15_000


def _extract_from_selectors(page: Page) -> str | None:
    for selector in _COUNT_SELECTORS:
        el = page.query_selector(selector)
        if el:
            text = el.inner_text().strip()
            if text and _OGLASA_RE.search(text):
                return text
    return None


def _extract_from_text(page: Page) -> str | None:
    """Fallback: search all visible text for 'N oglasa' pattern."""
    loc = page.locator("text=/\\d+\\s+oglas/i").first
    try:
        loc.wait_for(timeout=5_000)
        return loc.inner_text().strip()
    except Exception:
        return None


class IndexProvider(BaseProvider):
    """Headless-browser scraper for Index Oglasi (JavaScript-rendered SPA)."""

    def fetch_count(self, url: str) -> int:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            try:
                page = browser.new_page()
                page.goto(url, wait_until="networkidle", timeout=_NAV_TIMEOUT)

                text = _extract_from_selectors(page)
                if not text:
                    text = _extract_from_text(page)
            finally:
                browser.close()

        return self._parse_count(text, url)

    def scrape(
        self, categories: dict[str, str]
    ) -> tuple[list[ScrapeResult], dict[str, str]]:
        """Scrape all categories using a single browser instance."""
        results: list[ScrapeResult] = []
        errors: dict[str, str] = {}

        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            try:
                for name, url in categories.items():
                    try:
                        page = browser.new_page()
                        page.goto(url, wait_until="networkidle", timeout=_NAV_TIMEOUT)

                        text = _extract_from_selectors(page)
                        if not text:
                            text = _extract_from_text(page)
                        page.close()

                        count = self._parse_count(text, url)
                        results.append(ScrapeResult(category=name, count=count, url=url))
                    except Exception as exc:  # noqa: BLE001
                        print(f"[ERROR] IndexProvider: failed to scrape '{name}': {exc}")
                        errors[name] = str(exc)
            finally:
                browser.close()

        return results, errors

    @staticmethod
    def _parse_count(text: str | None, url: str) -> int:
        if not text:
            raise ScrapeError(f"Count element not found on {url}")

        match = _OGLASA_RE.search(text)
        if match is None:
            raise ScrapeError(
                f"Cannot extract count from '{text}' on {url}"
            )

        digits = match.group(1).replace(".", "")
        try:
            return int(digits)
        except ValueError as exc:
            raise ScrapeError(f"Cannot parse count '{match.group(1)}' as int") from exc
