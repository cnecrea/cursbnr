"""DataUpdateCoordinator pentru integrarea Curs valutar BNR."""
from __future__ import annotations

import logging
import time
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

from .const import DOMAIN, SECTIONS, UPDATE_HOUR_END, UPDATE_HOUR_START, URL
from .helpers import section_summary

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
        # ultima eroare raportată pe secțiune — avertismentul apare o dată, nu la fiecare actualizare
        self._section_errors: dict[str, str] = {}
        self.last_fetch: dict[str, Any] = {}

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
        except Exception as err:
            # Dacă avem date vechi, le returnăm în loc să dăm eroare
            if self.data is not None:
                _LOGGER.warning(
                    "Eroare la preluarea datelor, se păstrează datele anterioare: %s",
                    err,
                )
                return self.data
            raise UpdateFailed(f"Eroare la preluarea datelor BNR: {err}") from err

        self._log_sections(data)
        return data

    async def _fetch_data(self) -> dict[str, Any]:
        """Preia datele JSON de la API."""
        session = async_get_clientsession(self.hass)
        started = time.monotonic()
        _LOGGER.debug("Se preiau datele de la %s", URL)

        try:
            async with session.get(URL, timeout=30) as response:
                elapsed_ms = (time.monotonic() - started) * 1000
                if response.status != 200:
                    _LOGGER.debug("Răspuns HTTP %s în %.0f ms", response.status, elapsed_ms)
                    raise UpdateFailed(
                        f"Eroare HTTP {response.status} la preluarea datelor"
                    )
                raw = await response.read()
                data = await response.json(content_type=None)
        except UpdateFailed:
            raise
        except Exception as err:
            _LOGGER.debug("Preluarea a eșuat după %.0f ms: %r", (time.monotonic() - started) * 1000, err)
            raise UpdateFailed(
                f"Eroare la comunicarea cu API-ul BNR: {err}"
            ) from err

        if not isinstance(data, dict):
            raise UpdateFailed("Răspunsul API-ului nu are formatul așteptat (lipsește obiectul JSON)")

        generated = (data.get("_meta") or {}).get("generated_at")
        self.last_fetch = {
            "at": dt_util.now().isoformat(),
            "http_status": 200,
            "elapsed_ms": round(elapsed_ms),
            "bytes": len(raw),
            "generated_at": generated,
        }
        _LOGGER.debug(
            "Datele au fost preluate: HTTP 200, %d octeți, %.0f ms; fișier generat pe server la %s",
            len(raw),
            elapsed_ms,
            generated or "necunoscut (server fără _meta)",
        )
        return data

    def _log_sections(self, data: dict[str, Any]) -> None:
        """Jurnalizează starea fiecărei surse; avertizează o singură dată când o sursă începe să dea eroare."""
        summary = section_summary(data)
        for key, info in summary.items():
            name = SECTIONS[key]
            status = info["status"]
            error = info.get("error")

            if status == "ok":
                _LOGGER.debug("%s: OK — date din %s%s", name, info.get("latest") or "?",
                              f", {info['rows']} rânduri" if "rows" in info else "")
            elif status == "stale":
                _LOGGER.debug("%s: serverul a păstrat datele anterioare (din %s); eroarea sursei: %s",
                              name, info.get("latest") or "?", error)
            elif status == "missing":
                _LOGGER.debug("%s: secțiunea lipsește din răspuns", name)
            else:
                _LOGGER.debug("%s: eroare la sursă: %s", name, error)

            # avertisment la apariția unei erori noi; info când sursa își revine
            if error and self._section_errors.get(key) != error:
                if status == "stale":
                    _LOGGER.warning("%s: sursa nu răspunde, se afișează ultimele date disponibile (%s). Detalii: %s",
                                    name, info.get("latest") or "?", error)
                else:
                    _LOGGER.warning("%s: datele nu sunt disponibile, senzorul este eliminat până revin. Detalii: %s",
                                    name, error)
                self._section_errors[key] = error
            elif not error and key in self._section_errors:
                _LOGGER.info("%s: datele sunt din nou disponibile", name)
                del self._section_errors[key]
