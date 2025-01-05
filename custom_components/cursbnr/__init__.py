"""Inițializarea integrării Curs valutar BNR."""
from datetime import datetime, time, timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.entity import Entity
import asyncio
import logging
import aiohttp
from .const import DOMAIN, DEFAULT_UPDATE_INTERVAL, URL

_LOGGER = logging.getLogger(__name__)


class AllDataCoordinator(DataUpdateCoordinator):
    """Coordinator unic pentru integrarea care aduce toate datele."""

    def __init__(self, hass, name, update_interval):
        """Inițializează coordonatorul."""
        super().__init__(
            hass,
            _LOGGER,
            name=name,
            update_interval=timedelta(seconds=update_interval),
        )
        self._hass = hass
        self._update_interval = update_interval
        self._first_run = True  # Permite actualizarea la prima inițiere

    async def _async_update_data(self):
        """Actualizează datele."""
        current_time = datetime.now().time()
        start_time = time(13, 0)
        end_time = time(17, 0)

        if self._first_run:
            _LOGGER.debug("Prima inițiere - actualizarea datelor este permisă.")
        elif not (start_time <= current_time <= end_time):
            ora_curenta = datetime.now().strftime("%H:%M:%S")
            _LOGGER.debug(
                "Ora curentă (%s) este în afara intervalului permis (13:00 - 17:00). Actualizarea datelor este oprită.",
                ora_curenta,
            )
            return self.data  # Returnăm datele existente fără a face update

        _LOGGER.debug("Inițiem actualizarea datelor...")
        try:
            updated_data = await self._fetch_all_data()
            _LOGGER.debug("Actualizarea datelor a fost efectuată cu succes.")
            self._first_run = False  # Setăm _first_run la False după prima actualizare
            return updated_data
        except Exception as eroare:
            _LOGGER.error("Eroare la actualizarea datelor: %s", eroare)
            raise eroare

    async def _fetch_all_data(self):
        """Funcție care preia toate datele necesare."""
        try:
            async with aiohttp.ClientSession() as sesiune:
                async with sesiune.get(URL) as raspuns:
                    if raspuns.status != 200:
                        _LOGGER.error(
                            "Eroare la descărcarea datelor. Cod status HTTP: %s",
                            raspuns.status,
                        )
                        raise Exception(f"Eroare HTTP {raspuns.status}")
                    date = await raspuns.json()
                    _LOGGER.debug("Datele au fost preluate cu succes: %s", date)
                    return date
        except Exception as eroare:
            _LOGGER.error("A apărut o eroare la preluarea datelor: %s", eroare)
            raise eroare

# În fișierul __init__.py, creează coordonatorul global
async def async_setup_entry(hass, config_entry):
    """Configurează integrarea cu un singur coordonator."""
    hass.data.setdefault(DOMAIN, {})
    
    update_interval = config_entry.options.get("scan_interval", DEFAULT_UPDATE_INTERVAL)
    
    coordinator = AllDataCoordinator(hass, name=DOMAIN, update_interval=update_interval)
    await coordinator.async_config_entry_first_refresh()
    
    hass.data[DOMAIN][config_entry.entry_id] = coordinator
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(config_entry, "sensor")
    )
    return True

async def async_unload_entry(hass, config_entry):
    """Dezactivează integrarea."""
    unload_ok = await hass.config_entries.async_forward_entry_unload(config_entry, "sensor")
    if unload_ok:
        hass.data[DOMAIN].pop(config_entry.entry_id)

    return unload_ok
