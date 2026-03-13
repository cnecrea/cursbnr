"""Senzori pentru integrarea Curs valutar BNR.

Senzorii se creează dinamic doar când datele sunt disponibile.
Când datele dispar, senzorii sunt eliminați complet din Home Assistant.
Când datele revin, senzorii sunt recreați automat.
"""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION, CURRENCY_SENSORS, DOMAIN, FX_SENSORS
from .coordinator import CursBnrCoordinator
from .helpers import (
    extract_currency_data,
    extract_euribor_data,
    extract_fx_data,
    extract_ircc_trimestrial_data,
    extract_ircc_zilnic_data,
    extract_robor_data,
    safe_float,
)

_LOGGER = logging.getLogger(__name__)


# ── Device info comun ──────────────────────────────────────────────
DEVICE_INFO = DeviceInfo(
    identifiers={(DOMAIN, "cursbnr")},
    name="Curs valutar BNR",
    manufacturer="Ciprian Nicolae (cnecrea)",
    model="Curs valutar BNR",
    entry_type=DeviceEntryType.SERVICE,
)


# ── Manager dinamic senzori ────────────────────────────────────────

class SensorManager:
    """Gestionează crearea și ștergerea dinamică a senzorilor.

    La fiecare actualizare a coordinator-ului:
    - Verifică ce date sunt disponibile
    - Creează senzori noi pentru datele care au apărut
    - Șterge complet senzorii pentru care datele au dispărut
    """

    def __init__(
        self,
        hass: HomeAssistant,
        coordinator: CursBnrCoordinator,
        async_add_entities: AddEntitiesCallback,
    ) -> None:
        """Inițializează managerul."""
        self.hass = hass
        self.coordinator = coordinator
        self._async_add_entities = async_add_entities
        self._tracked_entities: dict[str, BaseBnrSensor] = {}
        self._remove_listener: callback | None = None

    def start(self) -> None:
        """Pornește managerul: creează senzorii inițiali și ascultă update-uri."""
        self._sync_sensors()
        self._remove_listener = self.coordinator.async_add_listener(
            self._on_coordinator_update
        )

    def stop(self) -> None:
        """Oprește managerul și curăță listener-ul."""
        if self._remove_listener:
            self._remove_listener()
            self._remove_listener = None

    @callback
    def _on_coordinator_update(self) -> None:
        """Callback apelat la fiecare actualizare a coordinator-ului."""
        self._sync_sensors()

    @callback
    def _sync_sensors(self) -> None:
        """Sincronizează senzorii cu datele disponibile."""
        data = self.coordinator.data or {}
        available_keys = self._detect_available_keys(data)
        current_keys = set(self._tracked_entities.keys())

        # ── Senzori noi de creat ──
        to_add = available_keys - current_keys
        if to_add:
            new_entities = self._create_sensors(to_add, data)
            if new_entities:
                for entity in new_entities:
                    self._tracked_entities[entity.sensor_key] = entity
                self._async_add_entities(new_entities)
                _LOGGER.info(
                    "Senzori creați dinamic: %s",
                    ", ".join(e.sensor_key for e in new_entities),
                )

        # ── Senzori de eliminat ──
        to_remove = current_keys - available_keys
        if to_remove:
            self._remove_sensors(to_remove)

    def _detect_available_keys(self, data: dict[str, Any]) -> set[str]:
        """Detectează ce chei de senzori au date disponibile."""
        keys: set[str] = set()

        # Curs valutar BNR
        curs_actual = data.get("curs_valutar", {}).get("actual", [])
        available_currencies = {
            item.get("currency")
            for item in curs_actual
            if item.get("currency")
        }
        for currency, config in CURRENCY_SENSORS.items():
            if currency in available_currencies:
                keys.add(config["key"])

        # FX / CEC
        cec_data = data.get("cec", [])
        available_fx = {
            item.get("currency")
            for item in cec_data
            if item.get("currency")
        }
        for currency, config in FX_SENSORS.items():
            if currency in available_fx:
                keys.add(config["key"])

        # ROBOR
        if data.get("robor", []):
            keys.add("dobanda_robor")

        # EURIBOR
        if data.get("euribor", {}):
            keys.add("dobanda_euribor")

        # IRCC zilnic
        if data.get("ircc_zilnic", []):
            keys.add("ircc_zilnic")

        # IRCC trimestrial
        if data.get("ircc_trimestru", []):
            keys.add("ircc_trimestrial")

        return keys

    def _create_sensors(
        self, keys: set[str], data: dict[str, Any]
    ) -> list[BaseBnrSensor]:
        """Creează instanțele de senzori pentru cheile specificate."""
        entities: list[BaseBnrSensor] = []

        for currency, config in CURRENCY_SENSORS.items():
            if config["key"] in keys:
                entities.append(
                    BnrCurrencySensor(self.coordinator, currency, config)
                )

        for currency, config in FX_SENSORS.items():
            if config["key"] in keys:
                entities.append(
                    BnrFxSensor(self.coordinator, currency, config)
                )

        if "dobanda_robor" in keys:
            entities.append(RoborSensor(self.coordinator))
        if "dobanda_euribor" in keys:
            entities.append(EuriborSensor(self.coordinator))
        if "ircc_zilnic" in keys:
            entities.append(IrccZilnicSensor(self.coordinator))
        if "ircc_trimestrial" in keys:
            entities.append(IrccTrimestrialSensor(self.coordinator))

        return entities

    def _remove_sensors(self, keys: set[str]) -> None:
        """Elimină complet senzorii din HA (nu doar Unavailable)."""
        ent_reg = er.async_get(self.hass)

        for key in keys:
            entity = self._tracked_entities.pop(key, None)
            if entity is None:
                continue

            unique_id = f"{DOMAIN}_{key}"
            entity_id = ent_reg.async_get_entity_id("sensor", DOMAIN, unique_id)

            if entity_id:
                ent_reg.async_remove(entity_id)
                _LOGGER.info(
                    "Senzor eliminat complet: %s (datele nu mai sunt disponibile)",
                    entity_id,
                )
            else:
                _LOGGER.debug(
                    "Senzor %s nu a fost găsit în registru pentru eliminare",
                    key,
                )


# ── Setup ──────────────────────────────────────────────────────────

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Configurează platforma senzorilor cu management dinamic."""
    entry_data = hass.data[DOMAIN][entry.entry_id]
    coordinator: CursBnrCoordinator = entry_data["coordinator"]

    manager = SensorManager(hass, coordinator, async_add_entities)
    manager.start()

    # Salvează managerul pentru cleanup la unload
    entry_data["sensor_manager"] = manager

    _LOGGER.debug("Platforma senzorilor a fost configurată cu manager dinamic")


# ── Clasă de bază ──────────────────────────────────────────────────

class BaseBnrSensor(CoordinatorEntity[CursBnrCoordinator], SensorEntity):
    """Clasă de bază pentru toți senzorii BNR."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: CursBnrCoordinator,
        name: str,
        unique_id_suffix: str,
        icon: str,
    ) -> None:
        """Inițializează senzorul."""
        super().__init__(coordinator)
        self._attr_name = name
        self._attr_unique_id = f"{DOMAIN}_{unique_id_suffix}"
        self._attr_icon = icon
        self._attr_device_info = DEVICE_INFO
        self._sensor_key = unique_id_suffix

    @property
    def sensor_key(self) -> str:
        """Returnează cheia unică a senzorului pentru tracking."""
        return self._sensor_key


# ── Senzori curs valutar BNR ───────────────────────────────────────

class BnrCurrencySensor(BaseBnrSensor):
    """Senzor generic pentru cursul valutar BNR."""

    _attr_suggested_display_precision = 4

    def __init__(
        self,
        coordinator: CursBnrCoordinator,
        currency: str,
        config: dict[str, str],
    ) -> None:
        """Inițializează senzorul de curs valutar."""
        super().__init__(
            coordinator,
            name=config["name"],
            unique_id_suffix=config["key"],
            icon=config["icon"],
        )
        self._currency = currency

    @property
    def native_value(self) -> float | None:
        """Returnează cursul curent."""
        result = extract_currency_data(self.coordinator.data, self._currency)
        if result is None:
            return None
        current, _ = result
        return current

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Atribute suplimentare: valoare anterioară, schimbare."""
        result = extract_currency_data(self.coordinator.data, self._currency)
        if result is None:
            return {ATTR_ATTRIBUTION: ATTRIBUTION}

        current, previous = result
        change = current - previous if previous else 0.0
        change_pct = (change / previous * 100) if previous else 0.0

        return {
            "Valoare curentă": f"{current:.4f}",
            "Valoare anterioară": f"{previous:.4f}",
            "Schimbare": f"{change:.4f}",
            "Schimbare procentuală": f"{change_pct:.2f}",
            ATTR_ATTRIBUTION: ATTRIBUTION,
        }


# ── Senzori schimb valutar (FX / CEC) ─────────────────────────────

class BnrFxSensor(BaseBnrSensor):
    """Senzor generic pentru schimbul valutar CEC."""

    _attr_suggested_display_precision = 4

    def __init__(
        self,
        coordinator: CursBnrCoordinator,
        currency: str,
        config: dict[str, str],
    ) -> None:
        """Inițializează senzorul FX."""
        super().__init__(
            coordinator,
            name=config["name"],
            unique_id_suffix=config["key"],
            icon=config["icon"],
        )
        self._currency = currency

    @property
    def native_value(self) -> float | None:
        """Returnează rata de vânzare (sell)."""
        result = extract_fx_data(self.coordinator.data, self._currency)
        if result is None:
            return None
        sell, _ = result
        return sell

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Atribute: vânzare, cumpărare."""
        result = extract_fx_data(self.coordinator.data, self._currency)
        if result is None:
            return {ATTR_ATTRIBUTION: ATTRIBUTION}

        sell, buy = result
        return {
            "Vânzare": f"{sell:.4f}",
            "Cumpărare": f"{buy:.4f}",
            ATTR_ATTRIBUTION: ATTRIBUTION,
        }


# ── Senzor ROBOR ──────────────────────────────────────────────────

class RoborSensor(BaseBnrSensor):
    """Senzor pentru dobânda ROBOR."""

    def __init__(self, coordinator: CursBnrCoordinator) -> None:
        """Inițializează senzorul ROBOR."""
        super().__init__(
            coordinator,
            name="Dobânda ROBOR",
            unique_id_suffix="dobanda_robor",
            icon="mdi:calendar-multiselect-outline",
        )

    @property
    def native_value(self) -> str | None:
        """Returnează data extragerii ROBOR."""
        result = extract_robor_data(self.coordinator.data)
        if result is None:
            return None
        return result["data"]

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Atribute: rate ROBOR pe perioade."""
        result = extract_robor_data(self.coordinator.data)
        if result is None:
            return {ATTR_ATTRIBUTION: ATTRIBUTION}

        return {
            "1 lună": f"{result['1m']:.2f}",
            "3 luni": f"{result['3m']:.2f}",
            "6 luni": f"{result['6m']:.2f}",
            "12 luni": f"{result['12m']:.2f}",
            ATTR_ATTRIBUTION: ATTRIBUTION,
        }


# ── Senzor EURIBOR ─────────────────────────────────────────────────

class EuriborSensor(BaseBnrSensor):
    """Senzor pentru dobânda EURIBOR."""

    _attr_suggested_display_precision = 3

    def __init__(self, coordinator: CursBnrCoordinator) -> None:
        """Inițializează senzorul EURIBOR."""
        super().__init__(
            coordinator,
            name="Dobânda EURIBOR",
            unique_id_suffix="dobanda_euribor",
            icon="mdi:percent",
        )

    @property
    def native_value(self) -> float | None:
        """Returnează rata EURIBOR 1-week."""
        result = extract_euribor_data(self.coordinator.data)
        if result is None:
            return None
        return result["1w"]

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Atribute: rate EURIBOR pe perioade."""
        result = extract_euribor_data(self.coordinator.data)
        if result is None:
            return {ATTR_ATTRIBUTION: ATTRIBUTION}

        return {
            "1 lună": f"{result['1m']:.3f}",
            "3 luni": f"{result['3m']:.3f}",
            "6 luni": f"{result['6m']:.3f}",
            "12 luni": f"{result['12m']:.3f}",
            ATTR_ATTRIBUTION: ATTRIBUTION,
        }


# ── Senzor IRCC zilnic ─────────────────────────────────────────────

class IrccZilnicSensor(BaseBnrSensor):
    """Senzor pentru IRCC zilnic."""

    _attr_suggested_display_precision = 2

    def __init__(self, coordinator: CursBnrCoordinator) -> None:
        """Inițializează senzorul IRCC zilnic."""
        super().__init__(
            coordinator,
            name="IRCC zilnic",
            unique_id_suffix="ircc_zilnic",
            icon="mdi:calendar-clock",
        )

    @property
    def native_value(self) -> float | None:
        """Returnează valoarea IRCC zilnic curentă."""
        result = extract_ircc_zilnic_data(self.coordinator.data)
        if result is None:
            return None
        return result["current"]

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Atribute: modificare față de valoarea anterioară."""
        result = extract_ircc_zilnic_data(self.coordinator.data)
        if result is None:
            return {ATTR_ATTRIBUTION: ATTRIBUTION}

        attrs: dict[str, Any] = {ATTR_ATTRIBUTION: ATTRIBUTION}
        if result.get("change") is not None:
            attrs["Modificare"] = f"{result['change']:.2f}"
        return attrs


# ── Senzor IRCC trimestrial ────────────────────────────────────────

class IrccTrimestrialSensor(BaseBnrSensor):
    """Senzor pentru IRCC trimestrial."""

    _attr_suggested_display_precision = 2

    def __init__(self, coordinator: CursBnrCoordinator) -> None:
        """Inițializează senzorul IRCC trimestrial."""
        super().__init__(
            coordinator,
            name="IRCC trimestrial",
            unique_id_suffix="ircc_trimestrial",
            icon="mdi:calendar-month",
        )

    @property
    def native_value(self) -> float | None:
        """Returnează valoarea IRCC trimestrial curentă."""
        result = extract_ircc_trimestrial_data(self.coordinator.data)
        if result is None:
            return None
        return result["current"]

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Atribute: modificare față de trimestrul anterior."""
        result = extract_ircc_trimestrial_data(self.coordinator.data)
        if result is None:
            return {ATTR_ATTRIBUTION: ATTRIBUTION}

        attrs: dict[str, Any] = {ATTR_ATTRIBUTION: ATTRIBUTION}
        if result.get("change") is not None:
            attrs["Modificare"] = f"{result['change']:.2f}"
        return attrs
