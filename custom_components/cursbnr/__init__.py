"""Inițializarea integrării Curs valutar BNR."""
import logging
import aiohttp
from datetime import timedelta
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, URL, DEFAULT_UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)

# Inițializare domeniu
PLATFORMS = ["sensor"]

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Setează integrarea prin configuration.yaml (dacă e cazul)."""
    _LOGGER.debug("Inițializare %s prin configuration.yaml (nefolosit în prezent)", DOMAIN)
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Inițializează integrarea folosind o intrare din Config Flow."""
    _LOGGER.info("Config Flow inițializat pentru %s", DOMAIN)

    # Preia intervalul de actualizare din opțiuni sau folosește valoarea implicită
    update_interval = entry.options.get("update_interval", DEFAULT_UPDATE_INTERVAL)

    # Creează DataUpdateCoordinator pentru gestionarea actualizărilor periodice
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=f"{DOMAIN}_coordinator",
        update_method=_async_update_data,
        update_interval=timedelta(seconds=update_interval),
    )

    # Stochează coordinatorul în Home Assistant
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Pornește coordinatorul
    await coordinator.async_config_entry_first_refresh()

    # Adaugă platformele asociate (e.g., senzorii)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    _LOGGER.debug("Platformele %s au fost inițializate cu succes pentru %s", PLATFORMS, DOMAIN)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Dezinstalează o intrare configurată."""
    _LOGGER.info("Se dezinstalează intrarea de configurare pentru domeniul %s", DOMAIN)

    # Șterge coordinatorul din Home Assistant
    hass.data[DOMAIN].pop(entry.entry_id)

    # Dezinstalează platformele asociate
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unloaded:
        _LOGGER.info("Intrarea de configurare pentru %s a fost dezinstalată cu succes.", DOMAIN)
    else:
        _LOGGER.error("Dezinstalarea intrării de configurare pentru %s a eșuat.", DOMAIN)

    return unloaded

async def _async_update_data():
    """Metodă de actualizare a datelor."""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(URL) as response:
                if response.status != 200:
                    _LOGGER.error("Eroare la preluarea datelor de la API-ul BNR: %s", response.status)
                    return {}
                json_data = await response.json()
                #_LOGGER.debug("JSON preluat de la API-ul BNR: %s", json_data)
                return json_data
        except aiohttp.ClientError as client_error:
            _LOGGER.error("Eroare la conexiunea cu API-ul BNR: %s", client_error)
        except Exception as e:
            _LOGGER.error("Eroare neașteptată la procesarea JSON-ului de la API-ul BNR: %s", e)
        return {}