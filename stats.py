from __future__ import annotations

from datetime import datetime, timezone, timedelta
from html import escape as _html_escape

from config import CATEGORY_ORDER, DISPLAY_NAMES
from notifier import EMOJI_MAP

_TZ = timezone(timedelta(hours=2))
_REPORT_HOUR = 21
_REPORT_MINUTE_FROM = 0

EMPTY_STATS: dict = {
    "date": "",
    "total_runs": 0,
    "successful_scrapes": {},
    "failed_scrapes": {},
    "last_report_counts": {},
    "report_sent": False,
}


def _today() -> str:
    return datetime.now(_TZ).strftime("%Y-%m-%d")


def _now_hour() -> int:
    return datetime.now(_TZ).hour


def _now_time_str() -> str:
    return datetime.now(_TZ).strftime("%H:%M")


def ensure_stats(state: dict) -> dict:
    """Ensure _stats key exists and reset if it's a new day."""
    stats = state.get("_stats")
    if stats is None or stats.get("date") != _today():
        state["_stats"] = {**EMPTY_STATS, "date": _today()}
        if stats and stats.get("last_report_counts"):
            state["_stats"]["last_report_counts"] = stats["last_report_counts"]
    return state


def record_run(
    state: dict,
    successes: list[str],
    errors: dict[str, str],
) -> None:
    """Record one cron run into stats."""
    stats = state["_stats"]
    stats["total_runs"] = stats.get("total_runs", 0) + 1

    sc = stats.setdefault("successful_scrapes", {})
    for cat in successes:
        sc[cat] = sc.get(cat, 0) + 1

    fc = stats.setdefault("failed_scrapes", {})
    for cat, reason in errors.items():
        fc.setdefault(cat, []).append(f"{_now_time_str()} - {reason}")


def _now_minute() -> int:
    return datetime.now(_TZ).minute


def should_send_report(state: dict) -> bool:
    stats = state.get("_stats", {})
    if stats.get("report_sent", False):
        return False
    h, m = _now_hour(), _now_minute()
    return (h > _REPORT_HOUR) or (h == _REPORT_HOUR and m >= _REPORT_MINUTE_FROM)


def mark_report_sent(state: dict, current_counts: dict[str, int]) -> None:
    stats = state["_stats"]
    stats["report_sent"] = True
    stats["last_report_counts"] = dict(current_counts)


def build_daily_report(state: dict, current_counts: dict[str, int]) -> tuple[str, str]:
    """Return (message_text, error_file_content). error_file_content is empty if no errors."""
    h = _html_escape
    stats = state.get("_stats", {})
    date_str = datetime.now(_TZ).strftime("%d.%m.%Y.")
    total = stats.get("total_runs", 0)
    failed = stats.get("failed_scrapes", {})
    total_errors = sum(len(v) for v in failed.values())

    lines = [f"\U0001F4CA Dnevni izvje\u0161taj \u2014 {date_str}\n"]

    if total_errors == 0:
        lines.append(f"\u2705 {total}/{total} runova | Sve OK")
    else:
        error_summary: dict[str, int] = {}
        for cat, reasons in failed.items():
            error_summary[cat] = len(reasons)
        summary_parts = [
            f"{h(DISPLAY_NAMES.get(cat, cat))}: {cnt}x"
            for cat, cnt in error_summary.items()
        ]
        lines.append(f"\u2705 {total}/{total} runova | \u274C {total_errors} gre\u0161aka ({', '.join(summary_parts)})")

    error_lines: list[str] = []
    if total_errors > 0:
        error_lines.append(f"Greške -- {date_str}\n")
        for cat, reasons in failed.items():
            display = DISPLAY_NAMES.get(cat, cat)
            error_lines.append(f"--- {display} ({len(reasons)}x) ---")
            for reason in reasons:
                error_lines.append(f"  {reason.strip()}")
            error_lines.append("")

    last_counts = stats.get("last_report_counts", {})

    groups = [
        ("Njuškalo", [c for c in CATEGORY_ORDER if c.startswith("nj_")]),
        ("Index", [c for c in CATEGORY_ORDER if c.startswith("idx_")]),
        ("Plavi Oglasnik", [c for c in CATEGORY_ORDER if c.startswith("oglas_")]),
        ("Bijelo Jaje", [c for c in CATEGORY_ORDER if c.startswith("bj_")]),
    ]

    for group_name, cats in groups:
        lines.append(f"\n<b>{h(group_name)}</b>")
        for cat in cats:
            emoji = EMOJI_MAP.get(cat, "\U0001F4CB")
            short_name = h(DISPLAY_NAMES.get(cat, cat).replace(f"{group_name} ", ""))
            count = current_counts.get(cat, 0)
            suffix = "oglas" if count == 1 else "oglasa"

            prev = last_counts.get(cat)
            if prev is not None:
                diff = count - prev
                if diff > 0:
                    diff_str = f" (\U0001F7E2 +{diff})"
                elif diff < 0:
                    diff_str = f" (\U0001F534 {diff})"
                else:
                    diff_str = " (\u2014 0)"
            else:
                diff_str = ""

            lines.append(f"{emoji} {short_name}: {count} {suffix}{diff_str}")

    return "\n".join(lines), "\n".join(error_lines)
