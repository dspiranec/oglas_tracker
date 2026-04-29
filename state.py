from __future__ import annotations

import json
from pathlib import Path


def load_state(path: Path) -> dict[str, int]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return {k: int(v) for k, v in data.items()}
    except (json.JSONDecodeError, ValueError) as exc:
        print(f"[WARN] Corrupt state file, resetting: {exc}")
        return {}


def save_state(path: Path, state: dict[str, int]) -> None:
    path.write_text(
        json.dumps(state, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"[INFO] State saved to {path}")
