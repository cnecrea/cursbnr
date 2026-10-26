"""Integrarea Curs valutar BNR pentru Home Assistant."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv

from .const import CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL, DOMAIN, PLATFORMS
from .coordinator import CursBnrCoordinator

if TYPE_CHECKING:
    from .sensor import SensorManager

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


@dataclass
class CursBnrData:
    """Datele intrării: coordinator-ul și managerul senzorilor dinamici."""

    coordinator: CursBnrCoordinator
    sensor_manager: SensorManager | None = None


type CursBnrConfigEntry = ConfigEntry[CursBnrData]


async def async_setup_entry(hass: HomeAssistant, entry: CursBnrConfigEntry) -> bool:
    """Configurează integrarea dintr-o intrare Config Flow."""
    # Intervalul de actualizare din options (prioritar) sau din data
    update_interval = entry.options.get(
        CONF_UPDATE_INTERVAL,
        entry.data.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL),
    )
    _LOGGER.debug("Configurare: interval de actualizare %s s", update_interval)

    coordinator = CursBnrCoordinator(hass, update_interval=update_interval)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = CursBnrData(coordinator=coordinator)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Ascultă schimbările din options
    entry.async_on_unload(entry.add_update_listener(_async_update_listener))

    _LOGGER.debug("Integrarea Curs valutar BNR a fost configurată cu succes")
    return True


async def _async_update_listener(
    hass: HomeAssistant, entry: CursBnrConfigEntry
) -> None:
    """Gestionează actualizarea opțiunilor."""
    _LOGGER.debug("Opțiunile integrării au fost modificate, se reîncarcă")
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(
    hass: HomeAssistant, entry: CursBnrConfigEntry
) -> bool:
    """Dezactivează integrarea."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        _LOGGER.debug("Integrarea Curs valutar BNR a fost dezactivată cu succes")

    return unload_ok
