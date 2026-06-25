from __future__ import annotations

import re

from playwright.sync_api import sync_playwright

from providers.base import BaseProvider, ScrapeError, ScrapeResult

_COUNT_RE = re.compile(r"Ukupno prikazanih oglasa \((\d+)\)")
_NAV_TIMEOUT = 30_000


class OglasnikProvider(BaseProvider):
    """Headless-browser scraper for Plavi Oglasnik (Next.js SPA)."""

    def fetch_count(self, url: str) -> int:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            try:
                page = browser.new_page()
                page.goto(url, wait_until="networkidle", timeout=_NAV_TIMEOUT)
                text = page.inner_text("body")
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
                        text = page.inner_text("body")
                        page.close()

                        count = self._parse_count(text, url)
                        results.append(ScrapeResult(category=name, count=count, url=url))
                    except Exception as exc:  # noqa: BLE001
                        print(f"[ERROR] OglasnikProvider: failed to scrape '{name}': {exc}")
                        errors[name] = str(exc)
            finally:
                browser.close()

        return results, errors

    @staticmethod
    def _parse_count(text: str, url: str) -> int:
        match = _COUNT_RE.search(text)
        if match is None:
            raise ScrapeError(f"Count pattern not found on {url}")

        try:
            return int(match.group(1))
        except ValueError as exc:
            raise ScrapeError(f"Cannot parse count '{match.group(1)}' as int") from exc
