"""Oglas Tracker – main entry point.

Scrapes configured ad categories, detects count increases,
sends a Telegram notification when new ads appear,
and delivers a daily summary report at 21:00.
"""

from __future__ import annotations

import sys

from config import CATEGORIES, STATE_FILE
from notifier import Change, send_notification, send_telegram_message
from providers.njuskalo import NjuskaloProvider
from state import get_counts, load_state, save_state
from stats import (
    build_daily_report,
    ensure_stats,
    mark_report_sent,
    record_run,
    should_send_report,
)


def run() -> None:
    print("[INFO] Starting oglas tracker run")

    provider = NjuskaloProvider()
    results, errors = provider.scrape(CATEGORIES)

    state = load_state(STATE_FILE)
    state = ensure_stats(state)

    successes = [r.category for r in results]
    record_run(state, successes, errors)

    if not results and not errors:
        print("[WARN] No categories were processed")
        save_state(STATE_FILE, state)
        return

    prev_counts = get_counts(state)
    first_run = len(prev_counts) == 0

    if first_run:
        print("[INFO] First run – initialising state without sending notification")
        for r in results:
            state[r.category] = r.count
        save_state(STATE_FILE, state)
        return

    changes: list[Change] = []

    for result in results:
        old_count = prev_counts.get(result.category)
        state[result.category] = result.count

        if old_count is None:
            print(f"[INFO] New category '{result.category}' detected ({result.count} ads)")
            continue

        diff = result.count - old_count
        if diff > 0:
            print(f"[INFO] {result.category}: {old_count} → {result.count} (+{diff})")
            changes.append(Change(result.category, old_count, result.count))
        elif diff < 0:
            print(f"[INFO] {result.category}: {old_count} → {result.count} ({diff})")
        else:
            print(f"[INFO] {result.category}: no change ({result.count})")

    if changes:
        send_notification(changes)

    if should_send_report(state):
        current_counts = get_counts(state)
        report = build_daily_report(state, current_counts)
        if send_telegram_message(report):
            mark_report_sent(state, current_counts)
            print("[INFO] Daily report sent")

    save_state(STATE_FILE, state)
    print("[INFO] Run complete")


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as exc:
        print(f"[FATAL] Unhandled exception: {exc}")
        sys.exit(1)
