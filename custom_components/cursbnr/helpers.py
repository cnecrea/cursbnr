"""Funcții utilitare pentru integrarea Curs valutar BNR."""
from __future__ import annotations

import logging
from typing import Any

from .const import SECTIONS

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


def section(data: dict[str, Any] | None, key: str) -> Any:
    """Datele unei secțiuni din JSON, sau None dacă lipsesc ori serverul a raportat o eroare.

    Când o sursă nu răspunde, serverul pune în locul datelor `{"error": "…"}` — un dict
    nevid, deci „adevărat”; tratat ca listă, ar face senzorul să arunce excepții.
    """
    if not data:
        return None
    value = data.get(key)
    if not value or (isinstance(value, dict) and "error" in value):
        return None
    return value


def section_error(data: dict[str, Any] | None, key: str) -> str | None:
    """Mesajul de eroare al unei secțiuni: din secțiune sau din `_meta.errors` (date păstrate)."""
    if not data:
        return None
    value = data.get(key)
    if isinstance(value, dict) and isinstance(value.get("error"), str):
        return value["error"]
    errors = (data.get("_meta") or {}).get("errors") or {}
    return errors.get(key) if isinstance(errors, dict) else None


def section_is_stale(data: dict[str, Any] | None, key: str) -> bool:
    """Serverul n-a putut actualiza secțiunea și a păstrat datele de data trecută."""
    stale = ((data or {}).get("_meta") or {}).get("stale") or []
    return key in stale if isinstance(stale, list) else False


def section_summary(data: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    """Starea fiecărei secțiuni (ok / eroare / date vechi) și data celor mai noi date — pentru jurnal și diagnostic."""
    summary: dict[str, dict[str, Any]] = {}
    for key in SECTIONS:
        value = section(data, key)
        error = section_error(data, key)
        if value is None:
            summary[key] = {"status": "error" if error else "missing", "error": error}
            continue
        entry: dict[str, Any] = {
            "status": "stale" if section_is_stale(data, key) else "ok",
            "latest": _latest_date(key, value),
        }
        if isinstance(value, list):
            entry["rows"] = len(value)
        if error:
            entry["error"] = error
        summary[key] = entry
    return summary


def _latest_date(key: str, value: Any) -> str | None:
    """Data celor mai noi date dintr-o secțiune, așa cum o scrie sursa."""
    try:
        if key == "curs_valutar":
            actual = value.get("actual") or []
            return actual[0].get("date") if actual else None
        if key == "euribor":
            return next((v.get("date") for v in value.values() if isinstance(v, dict)), None)
        if key == "cec":
            return None  # pagina CEC nu are dată
        return value[0].get("Data") if value else None
    except (AttributeError, IndexError, KeyError, TypeError):
        return None


def extract_currency_data(
    data: dict[str, Any] | None, currency: str
) -> tuple[float, float] | None:
    """Extrage cursul curent și anterior pentru o monedă.

    Returnează (valoare_curentă, valoare_anterioară) sau None dacă datele lipsesc.
    """
    curs = section(data, "curs_valutar")
    if not isinstance(curs, dict):
        return None

    curs_actual = curs.get("actual") or []
    curs_anterior = curs.get("anterior") or []

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
    cec_data = section(data, "cec")
    if not isinstance(cec_data, list):
        return None

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
    robor_list = section(data, "robor")
    if not isinstance(robor_list, list):
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
    euribor = section(data, "euribor")
    if not isinstance(euribor, dict):
        _LOGGER.debug("Nu există date EURIBOR")
        return None

    return {
        "1w": safe_float((euribor.get("1-week") or {}).get("rate")),
        "1m": safe_float((euribor.get("1-month") or {}).get("rate")),
        "3m": safe_float((euribor.get("3-months") or {}).get("rate")),
        "6m": safe_float((euribor.get("6-months") or {}).get("rate")),
        "12m": safe_float((euribor.get("12-months") or {}).get("rate")),
    }


def _ircc_value(row: dict[str, Any]) -> Any:
    # PMZ_RT în JSON; PMRZ_IR e numele actual al coloanei la BNR (dacă serverul l-ar trimite direct)
    return row.get("PMZ_RT", row.get("PMRZ_IR"))


def extract_ircc_zilnic_data(
    data: dict[str, Any] | None,
) -> dict[str, float | None] | None:
    """Extrage datele IRCC zilnic.

    Returnează dict cu cheile: current, change sau None.
    """
    ircc_list = section(data, "ircc_zilnic")
    if not isinstance(ircc_list, list):
        _LOGGER.debug("Nu există date IRCC zilnic")
        return None

    current = safe_float(_ircc_value(ircc_list[0]))

    change = None
    if len(ircc_list) >= 2:
        previous = safe_float(_ircc_value(ircc_list[1]))
        change = current - previous

    return {"current": current, "change": change}


def extract_ircc_trimestrial_data(
    data: dict[str, Any] | None,
) -> dict[str, float | None] | None:
    """Extrage datele IRCC trimestrial.

    Returnează dict cu cheile: current, change sau None.
    """
    ircc_list = section(data, "ircc_trimestru")
    if not isinstance(ircc_list, list):
        _LOGGER.debug("Nu există date IRCC trimestrial")
        return None

    newest = ircc_list[0]
    current = safe_float(newest.get("PMRT_IR", "0"))

    change = None
    if len(ircc_list) >= 2:
        previous = safe_float(ircc_list[1].get("PMRT_IR", "0"))
        change = current - previous

    return {"current": current, "change": change}
