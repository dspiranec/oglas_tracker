from __future__ import annotations

import os
from dataclasses import dataclass

import requests

from config import ALL_CATEGORIES, DISPLAY_NAMES

_TELEGRAM_API = "https://api.telegram.org/bot{token}/sendMessage"
_REQUEST_TIMEOUT = 10

EMOJI_MAP: dict[str, str] = {
    "nj_auti": "\U0001F697",
    "nj_kuce": "\U0001F3E0",
    "nj_stanovi": "\U0001F3E2",
    "idx_auti": "\U0001F697",
    "idx_kuce": "\U0001F3E0",
    "idx_stanovi": "\U0001F3E2",
}


@dataclass(frozen=True)
class Change:
    category: str
    old_count: int
    new_count: int


def build_message(changes: list[Change]) -> str:
    lines = ["\U0001F6A8 Novi oglasi pronađeni!\n"]

    for c in changes:
        emoji = EMOJI_MAP.get(c.category, "\U0001F4CB")
        display = DISPLAY_NAMES.get(c.category, c.category)
        lines.append(f"{emoji} {display}: {c.old_count} → {c.new_count}")

    lines.append("\nProvjeri oglase:")
    for c in changes:
        display = DISPLAY_NAMES.get(c.category, c.category)
        url = ALL_CATEGORIES.get(c.category, "")
        lines.append(f"{display}: {url}")

    return "\n".join(lines)


def send_telegram_message(text: str) -> bool:
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")

    if not token or not chat_id:
        print("[ERROR] TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set")
        return False

    print(f"[INFO] Sending Telegram message to chat {chat_id}")

    try:
        resp = requests.post(
            _TELEGRAM_API.format(token=token),
            json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown", "disable_web_page_preview": True},
            timeout=_REQUEST_TIMEOUT,
        )
        if resp.ok:
            print("[INFO] Telegram message sent successfully")
            return True
        print(f"[ERROR] Telegram API returned {resp.status_code}: {resp.text}")
        return False
    except requests.RequestException as exc:
        print(f"[ERROR] Failed to send Telegram message: {exc}")
        return False


def send_notification(changes: list[Change]) -> bool:
    return send_telegram_message(build_message(changes))
