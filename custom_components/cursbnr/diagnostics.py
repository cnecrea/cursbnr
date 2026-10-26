"""Diagnostice pentru integrarea Curs valutar BNR."""
from __future__ import annotations

from typing import Any

from homeassistant.core import HomeAssistant

from . import CursBnrConfigEntry
from .const import UPDATE_HOUR_END, UPDATE_HOUR_START, URL
from .helpers import section, section_summary


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: CursBnrConfigEntry
) -> dict[str, Any]:
    """Returnează diagnosticele pentru o intrare de configurare."""
    coordinator = entry.runtime_data.coordinator
    data = coordinator.data or {}

    # Date din config entry (fără informații sensibile — integrarea nu are credențiale)
    config_data = {
        "entry_id": entry.entry_id,
        "title": entry.title,
        "data": dict(entry.data),
        "options": dict(entry.options),
    }

    # Starea coordinator-ului
    coordinator_info = {
        "last_update_success": coordinator.last_update_success,
        "update_interval_seconds": coordinator.update_interval.total_seconds()
        if coordinator.update_interval
        else None,
        "update_window": f"{UPDATE_HOUR_START}:00-{UPDATE_HOUR_END}:00",
        "source_url": URL,
        "last_fetch": coordinator.last_fetch,
    }

    # Câte elemente are fiecare secțiune (fără valori)
    raw_data: dict[str, Any] = {}
    curs = section(data, "curs_valutar")
    if isinstance(curs, dict):
        raw_data["curs_valutar"] = {
            "actual_currencies": [item.get("currency") for item in curs.get("actual") or []],
            "anterior_currencies": [item.get("currency") for item in curs.get("anterior") or []],
        }
    cec = section(data, "cec")
    if isinstance(cec, list):
        raw_data["cec"] = {"currencies": [item.get("currency") for item in cec]}
    euribor = section(data, "euribor")
    if isinstance(euribor, dict):
        raw_data["euribor"] = {"periods": list(euribor.keys())}
    for key in ("robor", "ircc_zilnic", "ircc_trimestru"):
        rows = section(data, key)
        if isinstance(rows, list):
            raw_data[key] = {"entries_count": len(rows), "columns": sorted(rows[0].keys()) if rows else []}

    # Senzori activi (din managerul dinamic)
    sensor_manager = entry.runtime_data.sensor_manager
    active_sensors: list[str] = []
    if sensor_manager:
        active_sensors = sorted(sensor_manager._tracked_entities.keys())

    return {
        "config": config_data,
        "coordinator": coordinator_info,
        "server": data.get("_meta") or "fără _meta (script vechi pe server)",
        "sections": section_summary(data),
        "active_sensors": active_sensors,
        "data_summary": raw_data,
    }
