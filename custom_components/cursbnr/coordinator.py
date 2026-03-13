"""DataUpdateCoordinator pentru integrarea Curs valutar BNR."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

from .const import DOMAIN, UPDATE_HOUR_END, UPDATE_HOUR_START, URL

_LOGGER = logging.getLogger(__name__)


class CursBnrCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator pentru preluarea datelor de la API-ul BNR."""

    def __init__(
        self,
        hass: HomeAssistant,
        update_interval: int,
    ) -> None:
        """Inițializează coordinator-ul."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=update_interval),
        )
        self._first_run: bool = True

    async def _async_update_data(self) -> dict[str, Any]:
        """Preia datele de la API.

        Actualizarea se face:
        - La prima rulare (indiferent de oră)
        - Între orele UPDATE_HOUR_START și UPDATE_HOUR_END
        - În afara intervalului, returnează datele existente
        """
        now = dt_util.now()
        current_hour = now.hour

        if self._first_run:
            _LOGGER.debug("Prima rulare - se preiau datele indiferent de oră")
        elif not (UPDATE_HOUR_START <= current_hour < UPDATE_HOUR_END):
            _LOGGER.debug(
                "Ora curentă (%s:%s) este în afara intervalului %s:00-%s:00. "
                "Se păstrează datele existente",
                now.strftime("%H"),
                now.strftime("%M"),
                UPDATE_HOUR_START,
                UPDATE_HOUR_END,
            )
            if self.data is not None:
                return self.data
            # Dacă nu avem date deloc, forțăm preluarea
            _LOGGER.debug("Nu există date anterioare, se forțează preluarea")

        try:
            data = await self._fetch_data()
            self._first_run = False
            return data
        except Exception as err:
            # Dacă avem date vechi, le returnăm în loc să dăm eroare
            if self.data is not None:
                _LOGGER.warning(
                    "Eroare la preluarea datelor, se păstrează datele anterioare: %s",
                    err,
                )
                return self.data
            raise UpdateFailed(f"Eroare la preluarea datelor BNR: {err}") from err

    async def _fetch_data(self) -> dict[str, Any]:
        """Preia datele JSON de la API."""
        session = async_get_clientsession(self.hass)

        try:
            async with session.get(URL, timeout=30) as response:
                if response.status != 200:
                    raise UpdateFailed(
                        f"Eroare HTTP {response.status} la preluarea datelor"
                    )
                data: dict[str, Any] = await response.json(content_type=None)
                _LOGGER.debug("Datele au fost preluate cu succes de la API")
                return data
        except UpdateFailed:
            raise
        except Exception as err:
            raise UpdateFailed(
                f"Eroare la comunicarea cu API-ul BNR: {err}"
            ) from err
