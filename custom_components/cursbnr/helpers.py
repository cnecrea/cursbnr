"""Funcții utilitare pentru integrarea Curs valutar BNR."""
from __future__ import annotations

import logging
from typing import Any

_LOGGER = logging.getLogger(__name__)


def safe_float(value: Any, default: float = 0.0) -> float:
    """Convertește o valoare la float în mod sigur.

    Gestionează:
    - Valori None
    - Stringuri cu virgulă în loc de punct (format românesc)
    - Valori invalide
    """
    if value is None:
        return default
    try:
        if isinstance(value, str):
            value = value.replace(",", ".")
        return float(value)
    except (ValueError, TypeError):
        _LOGGER.debug("Nu s-a putut converti valoarea '%s' la float", value)
        return default


def extract_currency_data(
    data: dict[str, Any] | None, currency: str
) -> tuple[float, float] | None:
    """Extrage cursul curent și anterior pentru o monedă.

    Returnează (valoare_curentă, valoare_anterioară) sau None dacă datele lipsesc.
    """
    if not data:
        return None

    curs_actual = data.get("curs_valutar", {}).get("actual", [])
    curs_anterior = data.get("curs_valutar", {}).get("anterior", [])

    actual_item = next(
        (item for item in curs_actual if item.get("currency") == currency), None
    )
    if actual_item is None:
        _LOGGER.debug("Nu există date curs valutar actual pentru %s", currency)
        return None

    current = safe_float(actual_item.get("rate"))
    if current == 0.0:
        _LOGGER.debug("Rata curentă pentru %s este 0 sau invalidă", currency)
        return None

    anterior_item = next(
        (item for item in curs_anterior if item.get("currency") == currency), {}
    )
    previous = safe_float(anterior_item.get("rate"))

    return (current, previous)


def extract_fx_data(
    data: dict[str, Any] | None, currency: str
) -> tuple[float, float] | None:
    """Extrage rata sell/buy pentru o monedă din datele CEC.

    Returnează (sell_rate, buy_rate) sau None dacă datele lipsesc.
    """
    if not data:
        return None

    cec_data = data.get("cec", [])
    fx_item = next(
        (item for item in cec_data if item.get("currency") == currency), None
    )

    if fx_item is None:
        _LOGGER.debug("Nu există date FX/CEC pentru %s", currency)
        return None

    sell = safe_float(fx_item.get("sell_rate"))
    buy = safe_float(fx_item.get("buy_rate"))

    if sell == 0.0 and buy == 0.0:
        _LOGGER.debug("Ratele FX pentru %s sunt 0 sau invalide", currency)
        return None

    return (sell, buy)


def extract_robor_data(data: dict[str, Any] | None) -> dict[str, Any] | None:
    """Extrage datele ROBOR.

    Returnează dict cu cheile: data, 1m, 3m, 6m, 12m sau None.
    """
    if not data:
        return None

    robor_list = data.get("robor", [])
    if not robor_list:
        _LOGGER.debug("Nu există date ROBOR")
        return None

    newest = robor_list[0]
    data_extragere = newest.get("Data")
    if not data_extragere:
        _LOGGER.debug("Lipsește câmpul 'Data' din datele ROBOR")
        return None

    return {
        "data": data_extragere,
        "1m": safe_float(newest.get("BBZ_BOR1M", "0")),
        "3m": safe_float(newest.get("BBZ_BOR3M", "0")),
        "6m": safe_float(newest.get("BBZ_BOR6M", "0")),
        "12m": safe_float(newest.get("BBZ_BOR12M", "0")),
    }


def extract_euribor_data(data: dict[str, Any] | None) -> dict[str, float] | None:
    """Extrage datele EURIBOR.

    Returnează dict cu cheile: 1w, 1m, 3m, 6m, 12m sau None.
    """
    if not data:
        return None

    euribor = data.get("euribor", {})
    if not euribor:
        _LOGGER.debug("Nu există date EURIBOR")
        return None

    week_data = euribor.get("1-week", {})
    rate_1w = safe_float(week_data.get("rate"))

    return {
        "1w": rate_1w,
        "1m": safe_float(euribor.get("1-month", {}).get("rate")),
        "3m": safe_float(euribor.get("3-months", {}).get("rate")),
        "6m": safe_float(euribor.get("6-months", {}).get("rate")),
        "12m": safe_float(euribor.get("12-months", {}).get("rate")),
    }


def extract_ircc_zilnic_data(
    data: dict[str, Any] | None,
) -> dict[str, float | None] | None:
    """Extrage datele IRCC zilnic.

    Returnează dict cu cheile: current, change sau None.
    """
    if not data:
        return None

    ircc_list = data.get("ircc_zilnic", [])
    if not ircc_list:
        _LOGGER.debug("Nu există date IRCC zilnic")
        return None

    newest = ircc_list[0]
    current = safe_float(newest.get("PMZ_RT"))

    change = None
    if len(ircc_list) >= 2:
        previous = safe_float(ircc_list[1].get("PMZ_RT"))
        change = current - previous

    return {"current": current, "change": change}


def extract_ircc_trimestrial_data(
    data: dict[str, Any] | None,
) -> dict[str, float | None] | None:
    """Extrage datele IRCC trimestrial.

    Returnează dict cu cheile: current, change sau None.
    """
    if not data:
        return None

    ircc_list = data.get("ircc_trimestru", [])
    if not ircc_list:
        _LOGGER.debug("Nu există date IRCC trimestrial")
        return None

    newest = ircc_list[0]
    current = safe_float(newest.get("PMRT_IR", "0"))

    change = None
    if len(ircc_list) >= 2:
        previous = safe_float(ircc_list[1].get("PMRT_IR", "0"))
        change = current - previous

    return {"current": current, "change": change}
