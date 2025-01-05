"""Senzor pentru integrarea Curs valutar BNR."""
import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.helpers.device_registry import DeviceEntryType

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

ATTRIBUTION = "Date furnizate de BNR prin www.syspro.ro"


async def async_setup_entry(hass, entry, async_add_entities):
    """Configurează senzorii pe baza unei intrări din Config Flow."""
    _LOGGER.debug("Configurare senzori pentru integrarea Curs valutar BNR.")
    coordinator = hass.data[DOMAIN][entry.entry_id]

    # Lista senzorilor disponibili
    sensors = [
        BnrRatesEur(coordinator),
        BnrRatesUsd(coordinator),
        BnrRatesChf(coordinator),
        BnrRatesGbp(coordinator),
        BnrFxRatesEur(coordinator),
        BnrFxRatesUsd(coordinator),
        BnrFxRatesChf(coordinator),
        BnrFxRatesGbp(coordinator),
        DobandaRobor(coordinator),
        DobandaEuribor(coordinator),
        IRCCzilnic(coordinator),
        IRCCTrimestrial(coordinator),
    ]

    # Adaugă toți senzorii din listă
    async_add_entities(sensors, True)

    # Logare dinamică
    sensor_names = [sensor.name for sensor in sensors]
    _LOGGER.debug("Senzorii adăugați pentru integrarea Curs valutar BNR: %s", sensor_names)


class BaseBnrSensor(CoordinatorEntity, SensorEntity):
    """Clasa de bază pentru senzorii cursului valutar BNR."""

    def __init__(self, coordinator, name, unique_id, entity_id, icon):
        """Inițializează senzorul."""
        super().__init__(coordinator)
        self._attr_name = name
        self._attr_unique_id = unique_id
        self._attr_entity_id = entity_id
        self._attr_icon = icon
        _LOGGER.debug("Senzorul %s a fost inițializat.", self._attr_name)

    @property
    def native_value(self):
        """Returnează valoarea principală a senzorului."""
        raise NotImplementedError

    @property
    def extra_state_attributes(self):
        """Returnează atributele suplimentare."""
        raise NotImplementedError

    @property
    def icon(self):
        """Returnează pictograma senzorului."""
        return self._attr_icon

    @property
    def device_info(self):
        """Informații despre dispozitiv pentru integrare."""
        return {
            "identifiers": {(DOMAIN, "cursbnr")},
            "name": "Curs valutar BNR",
            "manufacturer": "Ciprian Nicolae (cnecrea)",
            "model": "Curs valutar BNR",
            "entry_type": DeviceEntryType.SERVICE,
        }


class BnrRatesEur(BaseBnrSensor):
    """Clasa senzorului pentru rata EUR oferită de BNR."""

    def __init__(self, coordinator):
        super().__init__(
            coordinator,
            name="Curs valutar RON → EUR",
            unique_id=f"{DOMAIN}_bnr_rates_ron_eur",
            entity_id="sensor.bnr_rates_ron_eur",
            icon="mdi:currency-eur",
        )

    @property
    def native_value(self):
        """Returnează valoarea principală a senzorului."""
        json_data = self.coordinator.data
        curs_actual = json_data.get("curs_valutar", {}).get("actual", [])
        valoare_eur = next((item["rate"] for item in curs_actual if item["currency"] == "EUR"), None)
        if valoare_eur is not None:
            valoare = float(valoare_eur)
            _LOGGER.debug("Valoarea principală a senzorului %s este: %.4f", self._attr_name, valoare)
            return valoare
        _LOGGER.error("Nu am găsit rata EUR în JSON pentru senzorul %s.", self._attr_name)
        return None

    @property
    def extra_state_attributes(self):
        """Returnează atributele suplimentare."""
        json_data = self.coordinator.data
        curs_actual = json_data.get("curs_valutar", {}).get("actual", [])
        curs_anterior = json_data.get("curs_valutar", {}).get("anterior", [])
        eur_actual = next((item for item in curs_actual if item["currency"] == "EUR"), {})
        eur_anterior = next((item for item in curs_anterior if item["currency"] == "EUR"), {})

        valoare_curenta = float(eur_actual.get("rate", 0))
        valoare_anterioara = float(eur_anterior.get("rate", 0))
        schimbare = valoare_curenta - valoare_anterioara
        schimbare_procentuală = (schimbare / valoare_anterioara * 100) if valoare_anterioara else 0

        attributes = {
            "Valoare curentă": "%.4f" % valoare_curenta,
            "Valoare anterioară": "%.4f" % valoare_anterioara,
            "Schimbare": "%.4f" % schimbare,
            "Schimbare procentuală": "%.2f" % schimbare_procentuală,
            ATTR_ATTRIBUTION: ATTRIBUTION,
        }

        _LOGGER.debug("Atributele suplimentare pentru senzorul %s: %s", self._attr_name, attributes)
        return attributes


class BnrRatesUsd(BaseBnrSensor):
    """Clasa senzorului pentru rata USD oferită de BNR."""

    def __init__(self, coordinator):
        super().__init__(
            coordinator,
            name="Curs valutar RON → USD",
            unique_id=f"{DOMAIN}_bnr_rates_ron_usd",
            entity_id="sensor.bnr_rates_ron_usd",
            icon="mdi:currency-usd",
        )

    @property
    def native_value(self):
        """Returnează valoarea principală a senzorului."""
        json_data = self.coordinator.data
        curs_actual = json_data.get("curs_valutar", {}).get("actual", [])
        valoare_usd = next((item["rate"] for item in curs_actual if item["currency"] == "USD"), None)
        if valoare_usd is not None:
            valoare = float(valoare_usd)
            _LOGGER.debug("Valoarea principală a senzorului %s este: %.4f", self._attr_name, valoare)
            return valoare
        _LOGGER.error("Nu am găsit rata USD în JSON pentru senzorul %s.", self._attr_name)
        return None

    @property
    def extra_state_attributes(self):
        """Returnează atributele suplimentare."""
        json_data = self.coordinator.data
        curs_actual = json_data.get("curs_valutar", {}).get("actual", [])
        curs_anterior = json_data.get("curs_valutar", {}).get("anterior", [])
        usd_actual = next((item for item in curs_actual if item["currency"] == "USD"), {})
        usd_anterior = next((item for item in curs_anterior if item["currency"] == "USD"), {})

        valoare_curenta = float(usd_actual.get("rate", 0))
        valoare_anterioara = float(usd_anterior.get("rate", 0))
        schimbare = valoare_curenta - valoare_anterioara
        schimbare_procentuală = (schimbare / valoare_anterioara * 100) if valoare_anterioara else 0

        attributes = {
            "Valoare curentă": "%.4f" % valoare_curenta,
            "Valoare anterioară": "%.4f" % valoare_anterioara,
            "Schimbare": "%.4f" % schimbare,
            "Schimbare procentuală": "%.2f" % schimbare_procentuală,
            ATTR_ATTRIBUTION: ATTRIBUTION,
        }

        _LOGGER.debug("Atributele suplimentare pentru senzorul %s: %s", self._attr_name, attributes)
        return attributes


class BnrRatesChf(BaseBnrSensor):
    """Clasa senzorului pentru rata CHF oferită de BNR."""

    def __init__(self, coordinator):
        super().__init__(
            coordinator,
            name="Curs valutar RON → CHF",
            unique_id=f"{DOMAIN}_bnr_rates_ron_chf",
            entity_id="sensor.bnr_rates_ron_chf",
            icon="mdi:cash",
        )

    @property
    def native_value(self):
        """Returnează valoarea principală a senzorului."""
        json_data = self.coordinator.data
        curs_actual = json_data.get("curs_valutar", {}).get("actual", [])
        valoare_chf = next((item["rate"] for item in curs_actual if item["currency"] == "CHF"), None)
        if valoare_chf is not None:
            valoare = float(valoare_chf)
            _LOGGER.debug("Valoarea principală a senzorului %s este: %.4f", self._attr_name, valoare)
            return valoare
        _LOGGER.error("Nu am găsit rata CHF în JSON pentru senzorul %s.", self._attr_name)
        return None

    @property
    def extra_state_attributes(self):
        """Returnează atributele suplimentare."""
        json_data = self.coordinator.data
        curs_actual = json_data.get("curs_valutar", {}).get("actual", [])
        curs_anterior = json_data.get("curs_valutar", {}).get("anterior", [])
        chf_actual = next((item for item in curs_actual if item["currency"] == "CHF"), {})
        chf_anterior = next((item for item in curs_anterior if item["currency"] == "CHF"), {})

        valoare_curenta = float(chf_actual.get("rate", 0))
        valoare_anterioara = float(chf_anterior.get("rate", 0))
        schimbare = valoare_curenta - valoare_anterioara
        schimbare_procentuală = (schimbare / valoare_anterioara * 100) if valoare_anterioara else 0

        attributes = {
            "Valoare curentă": "%.4f" % valoare_curenta,
            "Valoare anterioară": "%.4f" % valoare_anterioara,
            "Schimbare": "%.4f" % schimbare,
            "Schimbare procentuală": "%.2f" % schimbare_procentuală,
            ATTR_ATTRIBUTION: ATTRIBUTION,
        }

        _LOGGER.debug("Atributele suplimentare pentru senzorul %s: %s", self._attr_name, attributes)
        return attributes


class BnrRatesGbp(BaseBnrSensor):
    """Clasa senzorului pentru rata GBP oferită de BNR."""

    def __init__(self, coordinator):
        super().__init__(
            coordinator,
            name="Curs valutar RON → GBP",
            unique_id=f"{DOMAIN}_bnr_rates_ron_gbp",
            entity_id="sensor.bnr_rates_ron_gbp",
            icon="mdi:currency-gbp",
        )

    @property
    def native_value(self):
        """Returnează valoarea principală a senzorului."""
        json_data = self.coordinator.data
        curs_actual = json_data.get("curs_valutar", {}).get("actual", [])
        valoare_gbp = next((item["rate"] for item in curs_actual if item["currency"] == "GBP"), None)
        if valoare_gbp is not None:
            valoare = float(valoare_gbp)
            _LOGGER.debug("Valoarea principală a senzorului %s este: %.4f", self._attr_name, valoare)
            return valoare
        _LOGGER.error("Nu am găsit rata GBP în JSON pentru senzorul %s.", self._attr_name)
        return None

    @property
    def extra_state_attributes(self):
        """Returnează atributele suplimentare."""
        json_data = self.coordinator.data
        curs_actual = json_data.get("curs_valutar", {}).get("actual", [])
        curs_anterior = json_data.get("curs_valutar", {}).get("anterior", [])
        gbp_actual = next((item for item in curs_actual if item["currency"] == "GBP"), {})
        gbp_anterior = next((item for item in curs_anterior if item["currency"] == "GBP"), {})

        valoare_curenta = float(gbp_actual.get("rate", 0))
        valoare_anterioara = float(gbp_anterior.get("rate", 0))
        schimbare = valoare_curenta - valoare_anterioara
        schimbare_procentuală = (schimbare / valoare_anterioara * 100) if valoare_anterioara else 0

        attributes = {
            "Valoare curentă": "%.4f" % valoare_curenta,
            "Valoare anterioară": "%.4f" % valoare_anterioara,
            "Schimbare": "%.4f" % schimbare,
            "Schimbare procentuală": "%.2f" % schimbare_procentuală,
            ATTR_ATTRIBUTION: ATTRIBUTION,
        }

        _LOGGER.debug("Atributele suplimentare pentru senzorul %s: %s", self._attr_name, attributes)
        return attributes


class BnrFxRatesEur(BaseBnrSensor):
    """Clasa senzorului pentru rata EUR (FX Rates - Cash)."""

    def __init__(self, coordinator):
        super().__init__(
            coordinator,
            name="Schimb valutar RON → EUR",
            unique_id=f"{DOMAIN}_fx_rates_cash_eur",
            entity_id="sensor.fx_rates_cash_eur",
            icon="mdi:currency-eur",
        )

    @property
    def native_value(self):
        """Returnează valoarea principală a senzorului."""
        json_data = self.coordinator.data
        cec_data = json_data.get("cec", [])
        eur_data = next((item for item in cec_data if item["currency"] == "EUR"), {})

        sell_rate = eur_data.get("sell_rate", 0)
        if sell_rate:
            valoare = float(sell_rate)
            _LOGGER.debug("Valoarea principală a senzorului %s (Sell Rate) este: %.4f", self._attr_name, valoare)
            return valoare
        _LOGGER.error("Nu am găsit rata de vânzare pentru EUR în JSON pentru senzorul %s.", self._attr_name)
        return None

    @property
    def extra_state_attributes(self):
        """Returnează atributele suplimentare."""
        json_data = self.coordinator.data
        cec_data = json_data.get("cec", [])
        eur_data = next((item for item in cec_data if item["currency"] == "EUR"), {})

        if not eur_data:
            _LOGGER.debug("Nu există date pentru atributele senzorului %s.", self._attr_name)
            return {}

        attributes = {
            "Vânzare": "%.4f" % float(eur_data.get("sell_rate", 0)),
            "Cumpărare": "%.4f" % float(eur_data.get("buy_rate", 0)),
            ATTR_ATTRIBUTION: ATTRIBUTION,
        }

        _LOGGER.debug("Atributele suplimentare pentru senzorul %s: %s", self._attr_name, attributes)
        return attributes


class BnrFxRatesUsd(BaseBnrSensor):
    """Clasa senzorului pentru rata USD (FX Rates - Cash)."""

    def __init__(self, coordinator):
        super().__init__(
            coordinator,
            name="Schimb valutar RON → USD",
            unique_id=f"{DOMAIN}_fx_rates_cash_usd",
            entity_id="sensor.fx_rates_cash_usd",
            icon="mdi:currency-usd",
        )

    @property
    def native_value(self):
        """Returnează valoarea principală a senzorului."""
        json_data = self.coordinator.data
        cec_data = json_data.get("cec", [])
        usd_data = next((item for item in cec_data if item["currency"] == "USD"), {})

        sell_rate = usd_data.get("sell_rate", 0)
        if sell_rate:
            valoare = float(sell_rate)
            _LOGGER.debug("Valoarea principală a senzorului %s (Sell Rate) este: %.4f", self._attr_name, valoare)
            return valoare
        _LOGGER.error("Nu am găsit rata de vânzare pentru USD în JSON pentru senzorul %s.", self._attr_name)
        return None

    @property
    def extra_state_attributes(self):
        """Returnează atributele suplimentare."""
        json_data = self.coordinator.data
        cec_data = json_data.get("cec", [])
        usd_data = next((item for item in cec_data if item["currency"] == "USD"), {})

        if not usd_data:
            _LOGGER.debug("Nu există date pentru atributele senzorului %s.", self._attr_name)
            return {}

        attributes = {
            "Vânzare": "%.4f" % float(usd_data.get("sell_rate", 0)),
            "Cumpărare": "%.4f" % float(usd_data.get("buy_rate", 0)),
            ATTR_ATTRIBUTION: ATTRIBUTION,
        }

        _LOGGER.debug("Atributele suplimentare pentru senzorul %s: %s", self._attr_name, attributes)
        return attributes


class BnrFxRatesChf(BaseBnrSensor):
    """Clasa senzorului pentru rata CHF (FX Rates - Cash)."""

    def __init__(self, coordinator):
        super().__init__(
            coordinator,
            name="Schimb valutar RON → CHF",
            unique_id=f"{DOMAIN}_fx_rates_cash_chf",
            entity_id="sensor.fx_rates_cash_chf",
            icon="mdi:cash",
        )

    @property
    def native_value(self):
        """Returnează valoarea principală a senzorului."""
        json_data = self.coordinator.data
        cec_data = json_data.get("cec", [])
        chf_data = next((item for item in cec_data if item["currency"] == "CHF"), {})

        sell_rate = chf_data.get("sell_rate", 0)
        if sell_rate:
            valoare = float(sell_rate)
            _LOGGER.debug("Valoarea principală a senzorului %s (Sell Rate) este: %.4f", self._attr_name, valoare)
            return valoare
        _LOGGER.error("Nu am găsit rata de vânzare pentru CHF în JSON pentru senzorul %s.", self._attr_name)
        return None

    @property
    def extra_state_attributes(self):
        """Returnează atributele suplimentare."""
        json_data = self.coordinator.data
        cec_data = json_data.get("cec", [])
        chf_data = next((item for item in cec_data if item["currency"] == "CHF"), {})

        if not chf_data:
            _LOGGER.debug("Nu există date pentru atributele senzorului %s.", self._attr_name)
            return {}

        attributes = {
            "Vânzare": "%.4f" % float(chf_data.get("sell_rate", 0)),
            "Cumpărare": "%.4f" % float(chf_data.get("buy_rate", 0)),
            ATTR_ATTRIBUTION: ATTRIBUTION,
        }

        _LOGGER.debug("Atributele suplimentare pentru senzorul %s: %s", self._attr_name, attributes)
        return attributes


class BnrFxRatesGbp(BaseBnrSensor):
    """Clasa senzorului pentru rata GBP (FX Rates - Cash)."""

    def __init__(self, coordinator):
        super().__init__(
            coordinator,
            name="Schimb valutar RON → GBP",
            unique_id=f"{DOMAIN}_fx_rates_cash_gbp",
            entity_id="sensor.fx_rates_cash_gbp",
            icon="mdi:currency-gbp",
        )

    @property
    def native_value(self):
        """Returnează valoarea principală a senzorului."""
        json_data = self.coordinator.data
        cec_data = json_data.get("cec", [])
        gbp_data = next((item for item in cec_data if item["currency"] == "GBP"), {})

        sell_rate = gbp_data.get("sell_rate", 0)
        if sell_rate:
            valoare = float(sell_rate)
            _LOGGER.debug("Valoarea principală a senzorului %s (Sell Rate) este: %.4f", self._attr_name, valoare)
            return valoare
        _LOGGER.error("Nu am găsit rata de vânzare pentru GBP în JSON pentru senzorul %s.", self._attr_name)
        return None

    @property
    def extra_state_attributes(self):
        """Returnează atributele suplimentare."""
        json_data = self.coordinator.data
        cec_data = json_data.get("cec", [])
        gbp_data = next((item for item in cec_data if item["currency"] == "GBP"), {})

        if not gbp_data:
            _LOGGER.debug("Nu există date pentru atributele senzorului %s.", self._attr_name)
            return {}

        attributes = {
            "Vânzare": "%.4f" % float(gbp_data.get("sell_rate", 0)),
            "Cumpărare": "%.4f" % float(gbp_data.get("buy_rate", 0)),
            ATTR_ATTRIBUTION: ATTRIBUTION,
        }

        _LOGGER.debug("Atributele suplimentare pentru senzorul %s: %s", self._attr_name, attributes)
        return attributes


class DobandaEuribor(BaseBnrSensor):
    """Clasa senzorului pentru dobânda EURIBOR."""

    def __init__(self, coordinator):
        super().__init__(
            coordinator,
            name="Dobânda EURIBOR",
            unique_id=f"{DOMAIN}_dobanda_euribor",
            entity_id="sensor.dobanda_euribor",
            icon="mdi:percent",
        )

    @property
    def native_value(self):
        """Returnează valoarea principală a senzorului (dobânda EURIBOR 1-week)."""
        json_data = self.coordinator.data
        euribor_data = json_data.get("euribor", {}).get("1-week", {})
        valoare = float(euribor_data.get("rate", 0))
        _LOGGER.debug("Valoarea principală (native_value) a senzorului %s este: %.3f", self._attr_name, valoare)
        return valoare

    @property
    def extra_state_attributes(self):
        """Returnează atributele suplimentare."""
        json_data = self.coordinator.data
        euribor_data = json_data.get("euribor", {})
        if not euribor_data:
            _LOGGER.debug("Nu există date pentru atributele senzorului %s.", self._attr_name)
            return {}

        attributes = {
            "1 lună": "%.3f" % float(euribor_data.get("1-month", {}).get("rate", 0)),
            "3 luni": "%.3f" % float(euribor_data.get("3-months", {}).get("rate", 0)),
            "6 luni": "%.3f" % float(euribor_data.get("6-months", {}).get("rate", 0)),
            "12 luni": "%.3f" % float(euribor_data.get("12-months", {}).get("rate", 0)),
            ATTR_ATTRIBUTION: ATTRIBUTION,
        }
        _LOGGER.debug("Atributele suplimentare pentru senzorul %s (formatate cu 3 zecimale): %s", self._attr_name, attributes)
        return attributes


class DobandaRobor(BaseBnrSensor):
    """Clasa senzorului pentru dobânda ROBOR."""

    def __init__(self, coordinator):
        super().__init__(
            coordinator,
            name="Dobânda ROBOR",
            unique_id=f"{DOMAIN}_dobanda_robor",
            entity_id="sensor.dobanda_robor",
            icon="mdi:calendar-multiselect-outline",
        )

    @property
    def native_value(self):
        """Returnează valoarea principală a senzorului (data extragerii)."""
        json_data = self.coordinator.data
        robor_data = json_data.get("robor", [])

        if not robor_data:
            _LOGGER.error("Nu există date în JSON pentru senzorul %s.", self._attr_name)
            return None

        # Luăm data din primul element al listei (cel mai nou)
        data_extragere = robor_data[0].get("Data")
        if data_extragere:
            _LOGGER.debug("Valoarea principală (native_value) a senzorului %s este data: %s", self._attr_name, data_extragere)
            return data_extragere

        _LOGGER.error("Nu am găsit data pentru senzorul %s.", self._attr_name)
        return None

    @property
    def extra_state_attributes(self):
        """Returnează atributele suplimentare."""
        robor_data = self.coordinator.data.get("robor", [])

        if not robor_data:
            _LOGGER.debug("Nu există date pentru atributele senzorului %s.", self._attr_name)
            return {}

        # Luăm primul element din listă (cel mai nou)
        cel_mai_nou = robor_data[0]

        attributes = {
            "1 lună": "%.2f" % float(cel_mai_nou.get("BBZ_BOR1M", "0").replace(",", ".")),
            "3 luni": "%.2f" % float(cel_mai_nou.get("BBZ_BOR3M", "0").replace(",", ".")),
            "6 luni": "%.2f" % float(cel_mai_nou.get("BBZ_BOR6M", "0").replace(",", ".")),
            "12 luni": "%.2f" % float(cel_mai_nou.get("BBZ_BOR12M", "0").replace(",", ".")),
            ATTR_ATTRIBUTION: ATTRIBUTION,
        }

        _LOGGER.debug("Atributele suplimentare pentru senzorul %s: %s", self._attr_name, attributes)
        return attributes


class IRCCzilnic(BaseBnrSensor):
    """Clasa senzorului pentru IRCC zilnic."""

    def __init__(self, coordinator):
        super().__init__(
            coordinator,
            name="IRCC zilnic",
            unique_id=f"{DOMAIN}_ircc_zilnic",
            entity_id="sensor.ircc_zilnic",
            icon="mdi:calendar-clock",
        )

    @property
    def native_value(self):
        """Returnează valoarea principală a senzorului (PMZ_RT din cea mai recentă dată)."""
        json_data = self.coordinator.data
        ircc_data = json_data.get("ircc_zilnic", [])

        if not ircc_data or len(ircc_data) < 1:
            _LOGGER.error("Nu există date disponibile pentru senzorul %s.", self._attr_name)
            return None

        valoare = float(ircc_data[0].get("PMZ_RT").replace(",", "."))
        _LOGGER.debug("Valoarea principală (native_value) a senzorului %s este: %.2f", self._attr_name, valoare)
        return valoare

    @property
    def extra_state_attributes(self):
        """Returnează atributele suplimentare."""
        json_data = self.coordinator.data
        ircc_data = json_data.get("ircc_zilnic", [])

        if not ircc_data or len(ircc_data) < 2:
            _LOGGER.error("Nu există suficiente date pentru a calcula modificarea senzorului %s.", self._attr_name)
            return {}

        valoare_curenta = float(ircc_data[0].get("PMZ_RT").replace(",", "."))
        valoare_anterioara = float(ircc_data[1].get("PMZ_RT").replace(",", "."))
        modificare = valoare_curenta - valoare_anterioara

        attributes = {
            "Modificare": "%.2f" % modificare,
            ATTR_ATTRIBUTION: ATTRIBUTION,
        }

        _LOGGER.debug("Atributele suplimentare pentru senzorul %s: %s", self._attr_name, attributes)
        return attributes


class IRCCTrimestrial(BaseBnrSensor):
    """Clasa senzorului pentru IRCC Trimestrial."""

    def __init__(self, coordinator):
        super().__init__(
            coordinator,
            name="IRCC trimestrial",
            unique_id=f"{DOMAIN}_ircc_trimestrial",
            entity_id="sensor.ircc_trimestrial",
            icon="mdi:calendar-month",
        )

    @property
    def native_value(self):
        """Returnează valoarea principală a senzorului (PMRT_IR din cea mai recentă dată)."""
        json_data = self.coordinator.data
        ircc_data = json_data.get("ircc_trimestru", [])

        if ircc_data:
            valoare = float(ircc_data[0].get("PMRT_IR", "0").replace(",", "."))
            _LOGGER.debug("Valoarea principală (native_value) a senzorului %s este: %.2f", self._attr_name, valoare)
            return valoare

        _LOGGER.warning("Nu există date disponibile pentru senzorul %s.", self._attr_name)
        return None

    @property
    def extra_state_attributes(self):
        """Returnează atributele suplimentare."""
        json_data = self.coordinator.data
        ircc_data = json_data.get("ircc_trimestru", [])

        if len(ircc_data) < 2:
            _LOGGER.debug("Nu există suficiente date pentru atributele senzorului %s.", self._attr_name)
            return {}

        # Datele pentru cea mai recentă și cea anterioară valoare
        valoare_curenta = float(ircc_data[0].get("PMRT_IR", "0").replace(",", "."))
        valoare_anterioara = float(ircc_data[1].get("PMRT_IR", "0").replace(",", "."))

        # Calcul modificare
        modificare = valoare_curenta - valoare_anterioara

        attributes = {
            "Modificare": "%.2f" % modificare,
            ATTR_ATTRIBUTION: ATTRIBUTION,
        }

        _LOGGER.debug("Atributele suplimentare pentru senzorul %s: %s", self._attr_name, attributes)
        return attributes
