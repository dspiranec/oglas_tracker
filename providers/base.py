from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class ScrapeResult:
    category: str
    count: int
    url: str


class BaseProvider(ABC):
    """Every scraper provider must implement *fetch_count* for a single URL."""

    @abstractmethod
    def fetch_count(self, url: str) -> int:
        """Return the current number of ads visible on *url*.

        Raises ``ScrapeError`` when the page cannot be parsed.
        """

    def scrape(
        self, categories: dict[str, str]
    ) -> tuple[list[ScrapeResult], dict[str, str]]:
        """Scrape all *categories* and return results + errors.

        *categories* maps a human-readable name (e.g. ``"auti"``) to a URL.
        Individual failures are logged but never stop the remaining categories.

        Returns a tuple of (successful_results, errors_dict).
        """
        results: list[ScrapeResult] = []
        errors: dict[str, str] = {}
        for name, url in categories.items():
            try:
                count = self.fetch_count(url)
                results.append(ScrapeResult(category=name, count=count, url=url))
            except Exception as exc:  # noqa: BLE001
                print(f"[ERROR] {self.__class__.__name__}: failed to scrape '{name}': {exc}")
                errors[name] = str(exc)
        return results, errors


class ScrapeError(Exception):
    """Raised when a provider cannot extract the expected data."""
