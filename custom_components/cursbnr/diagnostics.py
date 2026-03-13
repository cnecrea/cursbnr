"""Diagnostice pentru integrarea Curs valutar BNR."""
from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import CursBnrCoordinator


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """Returnează diagnosticele pentru o intrare de configurare."""
    entry_data = hass.data[DOMAIN][entry.entry_id]
    coordinator: CursBnrCoordinator = entry_data["coordinator"]

    # Date din config entry (fără informații sensibile)
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
    }

    # Date brute de la API (anonimizate dacă e cazul)
    raw_data: dict[str, Any] = {}
    if coordinator.data:
        data = coordinator.data

        # Curs valutar - câte monede sunt disponibile
        curs_valutar = data.get("curs_valutar", {})
        actual = curs_valutar.get("actual", [])
        anterior = curs_valutar.get("anterior", [])
        raw_data["curs_valutar"] = {
            "actual_count": len(actual),
            "actual_currencies": [item.get("currency") for item in actual],
            "anterior_count": len(anterior),
            "anterior_currencies": [item.get("currency") for item in anterior],
        }

        # CEC/FX
        cec = data.get("cec", [])
        raw_data["cec"] = {
            "count": len(cec),
            "currencies": [item.get("currency") for item in cec],
        }

        # ROBOR
        robor = data.get("robor", [])
        raw_data["robor"] = {
            "entries_count": len(robor),
            "has_data": bool(robor),
        }

        # EURIBOR
        euribor = data.get("euribor", {})
        raw_data["euribor"] = {
            "periods": list(euribor.keys()) if euribor else [],
            "has_data": bool(euribor),
        }

        # IRCC
        ircc_zilnic = data.get("ircc_zilnic", [])
        raw_data["ircc_zilnic"] = {
            "entries_count": len(ircc_zilnic),
            "has_data": bool(ircc_zilnic),
        }

        ircc_trimestru = data.get("ircc_trimestru", [])
        raw_data["ircc_trimestru"] = {
            "entries_count": len(ircc_trimestru),
            "has_data": bool(ircc_trimestru),
        }

    # Senzori activi (din managerul dinamic)
    sensor_manager = entry_data.get("sensor_manager")
    active_sensors: list[str] = []
    if sensor_manager:
        active_sensors = sorted(sensor_manager._tracked_entities.keys())

    return {
        "config": config_data,
        "coordinator": coordinator_info,
        "active_sensors": active_sensors,
        "data_summary": raw_data,
    }
