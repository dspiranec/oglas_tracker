from __future__ import annotations

from pathlib import Path

STATE_FILE = Path(__file__).resolve().parent / "state.json"

NJUSKALO_CATEGORIES: dict[str, str] = {
    "nj_auti": (
        "https://www.njuskalo.hr/rabljeni-auti"
        "?vehicleIds=11710,11727,12945,15414"
        "&price[min]=1000&price[max]=10000"
        "&yearManufactured[min]=2010"
        "&adsWithImages=1"
        "&fuelTypeId=600"
        "&motorSize[min]=1250"
        "&motorPower[min]=70"
        "&mileage[max]=150000"
    ),
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
    "idx_auti": (
        "https://www.index.hr/oglasi/auto-moto/osobni-automobili/pretraga"
        "?searchQuery=%257B%2522category%2522%253A%2522osobni-automobili%2522"
        "%252C%2522makeYearFrom%2522%253A%25222009-12-31T23%253A00%253A00.000Z%2522"
        "%252C%2522fuelIds%2522%253A%255B2%255D"
        "%252C%2522powerFrom%2522%253A%252270%2522"
        "%252C%2522mileageTo%2522%253A%2522150000%2522"
        "%252C%2522cubicCapacityFrom%2522%253A%25221250%2522"
        "%252C%2522includeModelIds%2522%253A%255B"
        "%252221b4202e-abde-4e34-9f43-884af625e3bc%2522%252C"
        "%252205c67747-4f2a-4200-8b0f-ab71d677e170%2522%252C"
        "%2522d2226767-fcc2-4499-bfb1-d13da462f2cc%2522%252C"
        "%25224735081f-848a-4a6d-8fa2-1cde1843705f%2522%255D"
        "%252C%2522sortOption%2522%253A4"
        "%252C%2522module%2522%253A%2522auto-moto%2522"
        "%252C%2522priceTo%2522%253A%252210000%2522%257D"
    ),
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
    "nj_auti": "Njuškalo Auti",
    "nj_kuce": "Njuškalo Kuće",
    "nj_stanovi": "Njuškalo Stanovi",
    "idx_auti": "Index Auti",
    "idx_kuce": "Index Kuće",
    "idx_stanovi": "Index Stanovi",
    "oglas_stanovi": "Plavi Oglasnik Stanovi",
    "oglas_kuce": "Plavi Oglasnik Kuće",
    "bj_stanovi": "Bijelo Jaje Stanovi",
    "bj_kuce": "Bijelo Jaje Kuće",
}

CATEGORY_ORDER: list[str] = [
    "nj_auti", "nj_kuce", "nj_stanovi",
    "idx_auti", "idx_kuce", "idx_stanovi",
    "oglas_stanovi", "oglas_kuce",
    "bj_stanovi", "bj_kuce",
]
