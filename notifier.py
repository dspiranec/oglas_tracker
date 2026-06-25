from __future__ import annotations

import os
import tempfile
from dataclasses import dataclass
from html import escape as _html_escape

import requests

from config import ALL_CATEGORIES, DISPLAY_NAMES

_TELEGRAM_API = "https://api.telegram.org/bot{token}/{method}"
_REQUEST_TIMEOUT = 10

EMOJI_MAP: dict[str, str] = {
    "nj_auti": "\U0001F697",
    "nj_kuce": "\U0001F3E0",
    "nj_stanovi": "\U0001F3E2",
    "idx_auti": "\U0001F697",
    "idx_kuce": "\U0001F3E0",
    "idx_stanovi": "\U0001F3E2",
    "oglas_stanovi": "\U0001F3E2",
    "oglas_kuce": "\U0001F3E0",
    "bj_stanovi": "\U0001F3E2",
    "bj_kuce": "\U0001F3E0",
}


@dataclass(frozen=True)
class Change:
    category: str
    old_count: int
    new_count: int


def build_message(changes: list[Change]) -> str:
    h = _html_escape
    lines = ["\U0001F6A8 Novi oglasi pronađeni!\n"]

    for c in changes:
        emoji = EMOJI_MAP.get(c.category, "\U0001F4CB")
        display = h(DISPLAY_NAMES.get(c.category, c.category))
        lines.append(f"{emoji} {display}: {c.old_count} \u2192 {c.new_count}")

    lines.append("\nProvjeri oglase:")
    for c in changes:
        display = h(DISPLAY_NAMES.get(c.category, c.category))
        url = h(ALL_CATEGORIES.get(c.category, ""))
        lines.append(f"{display}: {url}")

    return "\n".join(lines)


def _get_credentials() -> tuple[str, str] | None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")
    if not token or not chat_id:
        print("[ERROR] TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set")
        return None
    return token, chat_id


def send_telegram_message(text: str) -> bool:
    creds = _get_credentials()
    if creds is None:
        return False
    token, chat_id = creds

    print(f"[INFO] Sending Telegram message to chat {chat_id}")

    try:
        resp = requests.post(
            _TELEGRAM_API.format(token=token, method="sendMessage"),
            json={"chat_id": chat_id, "text": text, "parse_mode": "HTML", "disable_web_page_preview": True},
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


def send_telegram_document(file_content: str, filename: str, caption: str = "") -> bool:
    creds = _get_credentials()
    if creds is None:
        return False
    token, chat_id = creds

    print(f"[INFO] Sending Telegram document '{filename}' to chat {chat_id}")

    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
            f.write(file_content)
            tmp_path = f.name

        data = {"chat_id": chat_id}
        if caption:
            data["caption"] = caption
            data["parse_mode"] = "HTML"

        with open(tmp_path, "rb") as f:
            resp = requests.post(
                _TELEGRAM_API.format(token=token, method="sendDocument"),
                data=data,
                files={"document": (filename, f, "text/plain")},
                timeout=_REQUEST_TIMEOUT,
            )

        os.unlink(tmp_path)

        if resp.ok:
            print("[INFO] Telegram document sent successfully")
            return True
        print(f"[ERROR] Telegram API returned {resp.status_code}: {resp.text}")
        return False
    except requests.RequestException as exc:
        print(f"[ERROR] Failed to send Telegram document: {exc}")
        return False


def send_notification(changes: list[Change]) -> bool:
    return send_telegram_message(build_message(changes))
