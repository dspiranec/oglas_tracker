from __future__ import annotations

from pathlib import Path

STATE_FILE = Path(__file__).resolve().parent / "state.json"

CATEGORIES: dict[str, str] = {
    "auti": (
        "https://www.njuskalo.hr/rabljeni-auti"
        "?vehicleIds=11710%2C11727%2C12945%2C15414"
        "&adsWithImages=1"
        "&price%5Bmin%5D=1000&price%5Bmax%5D=10000"
        "&yearManufactured%5Bmin%5D=2014"
        "&mileage%5Bmax%5D=150000"
        "&fuelTypeId=600"
        "&motorSize%5Bmin%5D=1250"
        "&motorPower%5Bmin%5D=70"
    ),
    "kuce": (
        "https://www.njuskalo.hr/prodaja-kuca"
        "?price%5Bmax%5D=270000"
        "&geo%5BlocationIds%5D=1731%2C1765%2C1766"
    ),
    "stanovi": (
        "https://www.njuskalo.hr/prodaja-stanova"
        "?geo[locationIds]=1731,1765,1766"
        "&price[max]=240000"
        "&livingArea[min]=35"
    ),
}

DISPLAY_NAMES: dict[str, str] = {
    "auti": "Auti",
    "kuce": "Kuće",
    "stanovi": "Stanovi",
}
