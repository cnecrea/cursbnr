"""Constante pentru integrarea Curs valutar BNR."""
from __future__ import annotations

from typing import Final

DOMAIN: Final = "cursbnr"

# URL pentru API-ul BNR
URL: Final = "http://130.61.61.84/homeassistant/cursbnr_data.json"

# Interval implicit de actualizare (în secunde)
DEFAULT_UPDATE_INTERVAL: Final = 300  # 5 minute

# Limitele intervalului de actualizare (în secunde)
MIN_UPDATE_INTERVAL: Final = 60    # 1 minut
MAX_UPDATE_INTERVAL: Final = 3600  # 60 de minute

# Interval orar pentru actualizare automată
UPDATE_HOUR_START: Final = 13
UPDATE_HOUR_END: Final = 17

# Atribuire
ATTRIBUTION: Final = "Date furnizate de BNR prin www.syspro.ro"

# Platforme suportate
PLATFORMS: Final = ["sensor"]

# Chei de configurare
CONF_UPDATE_INTERVAL: Final = "update_interval"

# Definiții senzori curs valutar BNR
CURRENCY_SENSORS: Final = {
    "EUR": {
        "name": "Curs valutar RON → EUR",
        "icon": "mdi:currency-eur",
        "key": "bnr_rates_ron_eur",
    },
    "USD": {
        "name": "Curs valutar RON → USD",
        "icon": "mdi:currency-usd",
        "key": "bnr_rates_ron_usd",
    },
    "CHF": {
        "name": "Curs valutar RON → CHF",
        "icon": "mdi:cash",
        "key": "bnr_rates_ron_chf",
    },
    "GBP": {
        "name": "Curs valutar RON → GBP",
        "icon": "mdi:currency-gbp",
        "key": "bnr_rates_ron_gbp",
    },
}

# Definiții senzori schimb valutar (FX / CEC)
FX_SENSORS: Final = {
    "EUR": {
        "name": "Schimb valutar RON → EUR",
        "icon": "mdi:currency-eur",
        "key": "fx_rates_cash_eur",
    },
    "USD": {
        "name": "Schimb valutar RON → USD",
        "icon": "mdi:currency-usd",
        "key": "fx_rates_cash_usd",
    },
    "CHF": {
        "name": "Schimb valutar RON → CHF",
        "icon": "mdi:cash",
        "key": "fx_rates_cash_chf",
    },
    "GBP": {
        "name": "Schimb valutar RON → GBP",
        "icon": "mdi:currency-gbp",
        "key": "fx_rates_cash_gbp",
    },
}
