from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, ValueError) as exc:
        print(f"[WARN] Corrupt state file, resetting: {exc}")
        return {}


def save_state(path: Path, state: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(state, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"[INFO] State saved to {path}")


def get_counts(state: dict[str, Any]) -> dict[str, int]:
    """Extract only ad-count entries (exclude _stats and other metadata)."""
    return {k: int(v) for k, v in state.items() if not k.startswith("_") and isinstance(v, (int, float))}
