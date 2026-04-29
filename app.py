"""Oglas Tracker – main entry point.

Scrapes configured ad categories, detects count increases,
and sends a Telegram notification when new ads appear.
"""

from __future__ import annotations

import sys

from config import CATEGORIES, STATE_FILE
from notifier import Change, send_notification, send_telegram_message
from providers.njuskalo import NjuskaloProvider
from state import load_state, save_state


def run() -> None:
    print("[INFO] Starting oglas tracker run")

    provider = NjuskaloProvider()
    results = provider.scrape(CATEGORIES)

    if not results:
        print("[WARN] No categories were successfully scraped")
        return

    prev_state = load_state(STATE_FILE)
    first_run = len(prev_state) == 0

    if first_run:
        print("[INFO] First run – initialising state without sending email")
        new_state = {r.category: r.count for r in results}
        save_state(STATE_FILE, new_state)
        return

    changes: list[Change] = []
    new_state = dict(prev_state)

    for result in results:
        old_count = prev_state.get(result.category)
        new_state[result.category] = result.count

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

    save_state(STATE_FILE, new_state)

    # TODO: obriši ovaj test blok nakon što potvrdiš da Telegram radi
    summary_lines = []
    for r in results:
        old = prev_state.get(r.category, "?")
        summary_lines.append(f"  {r.category}: {old} → {r.count}")
    send_telegram_message(
        "\u2705 Oglas Tracker run završen.\n\n"
        + "\n".join(summary_lines)
        + f"\n\nPromjene: {len(changes)}"
    )

    print("[INFO] Run complete")


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as exc:
        print(f"[FATAL] Unhandled exception: {exc}")
        sys.exit(1)
