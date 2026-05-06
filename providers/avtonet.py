from __future__ import annotations

import re
import time

from bs4 import BeautifulSoup
from curl_cffi import requests as cffi_requests
from playwright.sync_api import sync_playwright

from providers.base import BaseProvider, ScrapeError

_REQUEST_TIMEOUT = 20
_PRIKAZANO_RE = re.compile(r"Prikazano\s+(\d+)\s+oglas", re.IGNORECASE)
_NAV_TIMEOUT = 60_000
_CF_POLL_INTERVAL = 3
_CF_MAX_WAIT = 30


def _parse_count(html: str, url: str) -> int:
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


def _fetch_with_curl_cffi(url: str) -> str | None:
    """Fast path: curl_cffi impersonates Chrome TLS fingerprint."""
    try:
        resp = cffi_requests.get(url, impersonate="chrome", timeout=_REQUEST_TIMEOUT)
        if resp.status_code == 200 and "Prikazano" in resp.text:
            return resp.text
    except Exception as exc:
        print(f"[WARN] curl_cffi failed for avto.net: {exc}")
    return None


def _fetch_with_playwright(url: str) -> str | None:
    """Fallback: headless Chromium waits for Cloudflare challenge to resolve."""
    try:
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
                        return page.content()
                    if "Just a moment" not in page.title():
                        return page.content()
                    time.sleep(_CF_POLL_INTERVAL)
                    elapsed += _CF_POLL_INTERVAL

                return page.content()
            finally:
                browser.close()
    except Exception as exc:
        print(f"[WARN] Playwright fallback failed for avto.net: {exc}")
    return None


class AvtonetProvider(BaseProvider):
    """Scraper for Avto.net with curl_cffi (fast) + Playwright (fallback)."""

    def fetch_count(self, url: str) -> int:
        html = _fetch_with_curl_cffi(url)
        if html is None:
            print("[INFO] Trying Playwright fallback for avto.net")
            html = _fetch_with_playwright(url)

        if html is None:
            raise ScrapeError(f"All fetch methods failed for {url}")

        return _parse_count(html, url)
