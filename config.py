from __future__ import annotations

from pathlib import Path

STATE_FILE = Path(__file__).resolve().parent / "state.json"

NJUSKALO_CATEGORIES: dict[str, str] = {
    "nj_kuce": (
        "https://www.njuskalo.hr/prodaja-kuca"
        "?price%5Bmax%5D=340000"
        "&geo%5BlocationIds%5D=1731%2C1765%2C1766"
    ),
    "nj_stanovi": (
        "https://www.njuskalo.hr/prodaja-stanova"
        "?geo[locationIds]=1731,1765,1766"
        "&price[max]=240000"
        "&livingArea[min]=35"
    ),
}

INDEX_CATEGORIES: dict[str, str] = {
    "idx_kuce": (
        "https://www.index.hr/oglasi/nekretnine/prodaja-kuca/pretraga"
        "?searchQuery=%257B%2522category%2522%253A%2522houses-for-sale%2522"
        "%252C%2522module%2522%253A%2522real-estate%2522"
        "%252C%2522areaFrom%2522%253A%252235%2522"
        "%252C%2522priceTo%2522%253A%2522340000%2522"
        "%252C%2522sortOption%2522%253A4"
        "%252C%2522includeCityIds%2522%253A%255B"
        "%252233670252-7421-44f2-81fa-c13e2d7c971f%2522%252C"
        "%2522e0eefd1c-9cb5-41ee-a435-2bca97550031%2522%255D%257D"
    ),
    "idx_stanovi": (
        "https://www.index.hr/oglasi/nekretnine/flats-for-sale/pretraga"
        "?searchQuery=%257B%2522category%2522%253A%2522flats-for-sale%2522"
        "%252C%2522module%2522%253A%2522nekretnine%2522"
        "%252C%2522includeCityIds%2522%253A%255B"
        "%252233670252-7421-44f2-81fa-c13e2d7c971f%2522%252C"
        "%2522e0eefd1c-9cb5-41ee-a435-2bca97550031%2522%255D"
        "%252C%2522areaFrom%2522%253A%252235%2522"
        "%252C%2522priceTo%2522%253A%2522240000%2522"
        "%252C%2522sortOption%2522%253A4"
        "%252C%2522page%2522%253A1%257D"
    ),
}

OGLASNIK_CATEGORIES: dict[str, str] = {
    "oglas_stanovi": (
        "https://oglasnik.hr/stanovi-prodaja"
        "?f%5B4%5D%5B7760%5D=true&f%5B4%5D%5B7790%5D=true"
        "&f%5B4%5D%5B8495%5D=true&f%5B4%5D%5B8526%5D=true"
        "&f%5B2%5D%5Bmax%5D=250000&f%5B44%5D%5Bmin%5D=35"
    ),
    "oglas_kuce": (
        "https://oglasnik.hr/kuce-prodaja"
        "?f%5B4%5D%5B7760%5D=true&f%5B4%5D%5B7790%5D=true"
        "&f%5B4%5D%5B8495%5D=true&f%5B4%5D%5B8526%5D=true"
        "&f%5B2%5D%5Bmax%5D=340000"
    ),
}

BIJELOJAJE_CATEGORIES: dict[str, str] = {
    "bj_stanovi": (
        "https://bijelojaje.dnevnik.hr/oglasi/nekretnine/stanovi/prodaja-stanova"
        "/zagrebacka/brdovec~zapresic~zapresic-okolica/"
        "?attributes=dYNjpNlAmRGuWrvT%7E_250000"
        "%2CjnZdPJpcODuvrUwc%7E35_"
        "%2CusCFcVXhcFekamWN%7E_&page=1"
    ),
    "bj_kuce": (
        "https://bijelojaje.dnevnik.hr/oglasi/nekretnine/kuce/prodaja-kuca"
        "/zagrebacka/zapresic~brdovec~zapresic-okolica/"
        "?attributes=dYNjpNlAmRGuWrvT%7E_340000&page=1"
    ),
}

ALL_CATEGORIES: dict[str, str] = {
    **NJUSKALO_CATEGORIES,
    **INDEX_CATEGORIES,
    **OGLASNIK_CATEGORIES,
    **BIJELOJAJE_CATEGORIES,
}

DISPLAY_NAMES: dict[str, str] = {
    "nj_kuce": "Njuškalo Kuće",
    "nj_stanovi": "Njuškalo Stanovi",
    "idx_kuce": "Index Kuće",
    "idx_stanovi": "Index Stanovi",
    "oglas_stanovi": "Plavi Oglasnik Stanovi",
    "oglas_kuce": "Plavi Oglasnik Kuće",
    "bj_stanovi": "Bijelo Jaje Stanovi",
    "bj_kuce": "Bijelo Jaje Kuće",
}

CATEGORY_ORDER: list[str] = [
    "nj_kuce", "nj_stanovi",
    "idx_kuce", "idx_stanovi",
    "oglas_stanovi", "oglas_kuce",
    "bj_stanovi", "bj_kuce",
]
