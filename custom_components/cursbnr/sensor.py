"""Senzor pentru integrarea Curs valutar BNR."""
import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.helpers.device_registry import DeviceEntryType

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

ATTRIBUTION = "Date furnizate de BNR prin www.finradar.ro"


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

class BnrRatesEur(CoordinatorEntity, SensorEntity):
    """Clasa senzorului pentru rata EUR oferită de BNR."""

    def __init__(self, coordinator):
        """Inițializează senzorul."""
        super().__init__(coordinator)
        self._attr_name = "Curs valutar RON / EUR"
        self._attr_unique_id = f"{DOMAIN}_bnr_rates_ron_eur"
        self._attr_entity_id = "sensor.bnr_rates_ron_eur"

        _LOGGER.debug("Senzorul BnrRatesEur a fost inițializat.")

    @property
    def native_value(self):
        """Returnează valoarea principală a senzorului (currentValue)."""
        json_data = self.coordinator.data
        #_LOGGER.debug("JSON complet utilizat de BnrRatesEur: %s", json_data)

        valoare = float(json_data.get("pageProps", {}).get("bnrRates", {}).get("eur", {}).get("currentValue", 0))
        _LOGGER.debug("Valoarea principală a senzorului BnrRatesEur este: %.4f", valoare)
        return valoare

    @property
    def extra_state_attributes(self):
        """Returnează atributele suplimentare."""
        data = self.coordinator.data.get("pageProps", {}).get("bnrRates", {}).get("eur", {})
        if not data:
            _LOGGER.debug("Nu există date pentru atributele senzorului BnrRatesEur.")
            return {}

        attributes = {
            "Valoare curentă": "%.4f" % float(data.get("currentValue", 0)),
            "Valoare anterioară": "%.4f" % float(data.get("previousValue", 0)),
            "Schimbare": "%.4f" % float(data.get("change", 0)),
            "Schimbare procentuală": float(data.get("percentChange", 0)),
            ATTR_ATTRIBUTION: "Date furnizate de BNR prin www.finradar.ro",
        }
        _LOGGER.debug("Atribute brute (formatate cu 4 zecimale) înainte de returnare: %s", attributes)
        return attributes


        # Elimină câmpurile "lastArticles" și "lastPromos"
        data = {key: value for key, value in self.coordinator.data.items()
                if key not in ["lastArticles", "lastPromos"]}

        # Adaugă atributul "attribution"
        data[ATTR_ATTRIBUTION] = ATTRIBUTION

        _LOGGER.debug("Atributele senzorului BnrRatesEur au fost actualizate: %s", data)
        return data

    @property
    def unique_id(self):
        """Returnează identificatorul unic al senzorului."""
        return self._attr_unique_id

    @property
    def entity_id(self):
        """Returnează identificatorul explicit al entității."""
        return self._attr_entity_id

    @entity_id.setter
    def entity_id(self, value):
        """Setează identificatorul explicit al entității."""
        self._attr_entity_id = value
        _LOGGER.debug("Entity ID pentru senzorul BnrRatesEur a fost setat la: %s", value)

    @property
    def icon(self):
        """Pictograma senzorului."""
        return "mdi:currency-eur"

    @property
    def device_info(self):
        """Informații despre dispozitiv pentru integrare."""
        device_info = {
            "identifiers": {(DOMAIN, "cursbnr")},
            "name": "Curs valutar BNR",
            "manufacturer": "Ciprian Nicolae (cnecrea)",
            "model": "Curs valutar BNR",
            "entry_type": DeviceEntryType.SERVICE,
        }
        _LOGGER.debug("Informațiile dispozitivului pentru BnrRatesEur: %s", device_info)
        return device_info



class BnrRatesUsd(CoordinatorEntity, SensorEntity):
    """Clasa senzorului pentru rata USD oferită de BNR."""

    def __init__(self, coordinator):
        """Inițializează senzorul."""
        super().__init__(coordinator)
        self._attr_name = "Curs valutar RON / USD"
        self._attr_unique_id = f"{DOMAIN}_bnr_rates_ron_usd"
        self._attr_entity_id = "sensor.bnr_rates_ron_usd"

        _LOGGER.debug("Senzorul BnrRatesUsd a fost inițializat.")

    @property
    def native_value(self):
        """Returnează valoarea principală a senzorului (currentValue)."""
        json_data = self.coordinator.data
        valoare = float(json_data.get("pageProps", {}).get("bnrRates", {}).get("usd", {}).get("currentValue", 0))
        _LOGGER.debug("Valoarea principală a senzorului BnrRatesUsd este: %.4f", valoare)
        return valoare

    @property
    def extra_state_attributes(self):
        """Returnează atributele suplimentare."""
        data = self.coordinator.data.get("pageProps", {}).get("bnrRates", {}).get("usd", {})
        if not data:
            _LOGGER.debug("Nu există date pentru atributele senzorului BnrRatesUsd.")
            return {}

        attributes = {
            "Valoare curentă": "%.4f" % float(data.get("currentValue", 0)),
            "Valoare anterioară": "%.4f" % float(data.get("previousValue", 0)),
            "Schimbare": "%.4f" % float(data.get("change", 0)),
            "Schimbare procentuală": float(data.get("percentChange", 0)),
            ATTR_ATTRIBUTION: "Date furnizate de BNR prin www.finradar.ro",
        }
        _LOGGER.debug("Atributele senzorului BnrRatesUsd: %s", attributes)
        return attributes

    @property
    def unique_id(self):
        """Returnează identificatorul unic al senzorului."""
        return self._attr_unique_id

    @property
    def entity_id(self):
        """Returnează identificatorul explicit al entității."""
        return self._attr_entity_id

    @entity_id.setter
    def entity_id(self, value):
        """Setează identificatorul explicit al entității."""
        self._attr_entity_id = value
        _LOGGER.debug("Entity ID pentru senzorul BnrRatesUsd a fost setat la: %s", value)

    @property
    def icon(self):
        """Pictograma senzorului."""
        return "mdi:currency-usd"

    @property
    def device_info(self):
        """Informații despre dispozitiv pentru integrare."""
        device_info = {
            "identifiers": {(DOMAIN, "cursbnr")},
            "name": "Curs valutar BNR",
            "manufacturer": "Ciprian Nicolae (cnecrea)",
            "model": "Curs valutar BNR",
            "entry_type": DeviceEntryType.SERVICE,
        }
        _LOGGER.debug("Informațiile dispozitivului pentru BnrRatesUsd: %s", device_info)
        return device_info


class BnrRatesChf(CoordinatorEntity, SensorEntity):
    """Clasa senzorului pentru rata CHF oferită de BNR."""

    def __init__(self, coordinator):
        """Inițializează senzorul."""
        super().__init__(coordinator)
        self._attr_name = "Curs valutar RON / CHF"
        self._attr_unique_id = f"{DOMAIN}_bnr_rates_ron_chf"
        self._attr_entity_id = "sensor.bnr_rates_ron_chf"

        _LOGGER.debug("Senzorul BnrRatesChf a fost inițializat.")

    @property
    def native_value(self):
        """Returnează valoarea principală a senzorului (currentValue)."""
        json_data = self.coordinator.data
        valoare = float(json_data.get("pageProps", {}).get("bnrRates", {}).get("chf", {}).get("currentValue", 0))
        _LOGGER.debug("Valoarea principală a senzorului BnrRatesChf este: %.4f", valoare)
        return valoare

    @property
    def extra_state_attributes(self):
        """Returnează atributele suplimentare."""
        data = self.coordinator.data.get("pageProps", {}).get("bnrRates", {}).get("chf", {})
        if not data:
            _LOGGER.debug("Nu există date pentru atributele senzorului BnrRatesChf.")
            return {}

        attributes = {
            "Valoare curentă": "%.4f" % float(data.get("currentValue", 0)),
            "Valoare anterioară": "%.4f" % float(data.get("previousValue", 0)),
            "Schimbare": "%.4f" % float(data.get("change", 0)),
            "Schimbare procentuală": float(data.get("percentChange", 0)),
            ATTR_ATTRIBUTION: "Date furnizate de BNR prin www.finradar.ro",
        }
        _LOGGER.debug("Atributele senzorului BnrRatesChf: %s", attributes)
        return attributes

    @property
    def unique_id(self):
        """Returnează identificatorul unic al senzorului."""
        return self._attr_unique_id

    @property
    def entity_id(self):
        """Returnează identificatorul explicit al entității."""
        return self._attr_entity_id

    @entity_id.setter
    def entity_id(self, value):
        """Setează identificatorul explicit al entității."""
        self._attr_entity_id = value
        _LOGGER.debug("Entity ID pentru senzorul BnrRatesChf a fost setat la: %s", value)

    @property
    def icon(self):
        """Pictograma senzorului."""
        return "mdi:cash"

    @property
    def device_info(self):
        """Informații despre dispozitiv pentru integrare."""
        device_info = {
            "identifiers": {(DOMAIN, "cursbnr")},
            "name": "Curs valutar BNR",
            "manufacturer": "Ciprian Nicolae (cnecrea)",
            "model": "Curs valutar BNR",
            "entry_type": DeviceEntryType.SERVICE,
        }
        _LOGGER.debug("Informațiile dispozitivului pentru BnrRatesChf: %s", device_info)
        return device_info


class BnrRatesGbp(CoordinatorEntity, SensorEntity):
    """Clasa senzorului pentru rata GBP oferită de BNR."""

    def __init__(self, coordinator):
        """Inițializează senzorul."""
        super().__init__(coordinator)
        self._attr_name = "Curs valutar RON / GBP"
        self._attr_unique_id = f"{DOMAIN}_bnr_rates_ron_gbp"
        self._attr_entity_id = "sensor.bnr_rates_ron_gbp"

        _LOGGER.debug("Senzorul BnrRatesGbp a fost inițializat.")

    @property
    def native_value(self):
        """Returnează valoarea principală a senzorului (currentValue)."""
        json_data = self.coordinator.data
        valoare = float(json_data.get("pageProps", {}).get("bnrRates", {}).get("gbp", {}).get("currentValue", 0))
        _LOGGER.debug("Valoarea principală a senzorului BnrRatesGbp este: %.4f", valoare)
        return valoare

    @property
    def extra_state_attributes(self):
        """Returnează atributele suplimentare."""
        data = self.coordinator.data.get("pageProps", {}).get("bnrRates", {}).get("gbp", {})
        if not data:
            _LOGGER.debug("Nu există date pentru atributele senzorului BnrRatesGbp.")
            return {}

        attributes = {
            "Valoare curentă": "%.4f" % float(data.get("currentValue", 0)),
            "Valoare anterioară": "%.4f" % float(data.get("previousValue", 0)),
            "Schimbare": "%.4f" % float(data.get("change", 0)),
            "Schimbare procentuală": float(data.get("percentChange", 0)),
            ATTR_ATTRIBUTION: "Date furnizate de BNR prin www.finradar.ro",
        }
        _LOGGER.debug("Atributele senzorului BnrRatesGbp: %s", attributes)
        return attributes

    @property
    def unique_id(self):
        """Returnează identificatorul unic al senzorului."""
        return self._attr_unique_id

    @property
    def entity_id(self):
        """Returnează identificatorul explicit al entității."""
        return self._attr_entity_id

    @entity_id.setter
    def entity_id(self, value):
        """Setează identificatorul explicit al entității."""
        self._attr_entity_id = value
        _LOGGER.debug("Entity ID pentru senzorul BnrRatesGbp a fost setat la: %s", value)

    @property
    def icon(self):
        """Pictograma senzorului."""
        return "mdi:currency-gbp"

    @property
    def device_info(self):
        """Informații despre dispozitiv pentru integrare."""
        device_info = {
            "identifiers": {(DOMAIN, "cursbnr")},
            "name": "Curs valutar BNR",
            "manufacturer": "Ciprian Nicolae (cnecrea)",
            "model": "Curs valutar BNR",
            "entry_type": DeviceEntryType.SERVICE,
        }
        _LOGGER.debug("Informațiile dispozitivului pentru BnrRatesGbp: %s", device_info)
        return device_info


class BnrFxRatesEur(CoordinatorEntity, SensorEntity):
    """Clasa senzorului pentru rata EUR (FX Rates - Cash)."""

    def __init__(self, coordinator):
        """Inițializează senzorul."""
        super().__init__(coordinator)
        self._attr_name = "Schimb valutar RON / EUR"
        self._attr_unique_id = f"{DOMAIN}_fx_rates_cash_eur"
        self._attr_entity_id = "sensor.fx_rates_cash_eur"

        _LOGGER.debug("Senzorul BnrFxRatesEur a fost inițializat.")

    @property
    def native_value(self):
        """Returnează valoarea principală a senzorului."""
        json_data = self.coordinator.data
        valoare = float(json_data.get("pageProps", {}).get("fxRates", {}).get("cash", {}).get("eur", {}).get("sell", 0))
        _LOGGER.debug("Valoarea principală a senzorului BnrFxRatesEur este: %.4f", valoare)
        return valoare

    @property
    def extra_state_attributes(self):
        """Returnează atributele suplimentare."""
        data = self.coordinator.data.get("pageProps", {}).get("fxRates", {}).get("cash", {}).get("eur", {})
        if not data:
            _LOGGER.debug("Nu există date pentru atributele senzorului BnrFxRatesEur.")
            return {}

        attributes = {
            "Vânzare": "%.4f" % float(data.get("sell", 0)),
            "Cumpărare": "%.4f" % float(data.get("buy", 0)),
            ATTR_ATTRIBUTION: "Date furnizate de BNR prin www.finradar.ro",
        }
        _LOGGER.debug("Atributele senzorului BnrFxRatesEur: %s", attributes)
        return attributes

    @property
    def unique_id(self):
        """Returnează identificatorul unic al senzorului."""
        return self._attr_unique_id

    @property
    def entity_id(self):
        """Returnează identificatorul explicit al entității."""
        return self._attr_entity_id

    @entity_id.setter
    def entity_id(self, value):
        """Setează identificatorul explicit al entității."""
        self._attr_entity_id = value
        _LOGGER.debug("Entity ID pentru senzorul BnrFxRatesEur a fost setat la: %s", value)

    @property
    def icon(self):
        """Pictograma senzorului."""
        return "mdi:currency-eur"

    @property
    def device_info(self):
        """Informații despre dispozitiv pentru integrarea Schimb Valutar."""
        device_info = {
            "identifiers": {(DOMAIN, "schimbbnr")},
            "name": "Schimb valutar BNR",
            "manufacturer": "Ciprian Nicolae (cnecrea)",
            "model": "Schimb valutar BNR",
            "entry_type": DeviceEntryType.SERVICE,
        }
        _LOGGER.debug("Informațiile dispozitivului pentru BnrFxRatesEur: %s", device_info)
        return device_info


class BnrFxRatesUsd(CoordinatorEntity, SensorEntity):
    """Clasa senzorului pentru rata USD (FX Rates - Cash)."""

    def __init__(self, coordinator):
        """Inițializează senzorul."""
        super().__init__(coordinator)
        self._attr_name = "Schimb valutar RON / USD"
        self._attr_unique_id = f"{DOMAIN}_fx_rates_cash_usd"
        self._attr_entity_id = "sensor.fx_rates_cash_usd"

        _LOGGER.debug("Senzorul BnrFxRatesUsd a fost inițializat.")

    @property
    def native_value(self):
        """Returnează valoarea principală a senzorului."""
        json_data = self.coordinator.data
        valoare = float(json_data.get("pageProps", {}).get("fxRates", {}).get("cash", {}).get("usd", {}).get("sell", 0))
        _LOGGER.debug("Valoarea principală a senzorului BnrFxRatesUsd este: %.4f", valoare)
        return valoare

    @property
    def extra_state_attributes(self):
        """Returnează atributele suplimentare."""
        data = self.coordinator.data.get("pageProps", {}).get("fxRates", {}).get("cash", {}).get("usd", {})
        if not data:
            _LOGGER.debug("Nu există date pentru atributele senzorului BnrFxRatesUsd.")
            return {}

        attributes = {
            "Vânzare": "%.4f" % float(data.get("sell", 0)),
            "Cumpărare": "%.4f" % float(data.get("buy", 0)),
            ATTR_ATTRIBUTION: "Date furnizate de BNR prin www.finradar.ro",
        }
        _LOGGER.debug("Atributele senzorului BnrFxRatesUsd: %s", attributes)
        return attributes

    @property
    def unique_id(self):
        """Returnează identificatorul unic al senzorului."""
        return self._attr_unique_id

    @property
    def entity_id(self):
        """Returnează identificatorul explicit al entității."""
        return self._attr_entity_id

    @entity_id.setter
    def entity_id(self, value):
        """Setează identificatorul explicit al entității."""
        self._attr_entity_id = value
        _LOGGER.debug("Entity ID pentru senzorul BnrFxRatesUsd a fost setat la: %s", value)

    @property
    def icon(self):
        """Pictograma senzorului."""
        return "mdi:currency-usd"

    @property
    def device_info(self):
        """Informații despre dispozitiv pentru integrarea Schimb Valutar."""
        device_info = {
            "identifiers": {(DOMAIN, "schimbbnr")},
            "name": "Schimb valutar BNR",
            "manufacturer": "Ciprian Nicolae (cnecrea)",
            "model": "Schimb valutar BNR",
            "entry_type": DeviceEntryType.SERVICE,
        }
        _LOGGER.debug("Informațiile dispozitivului pentru BnrFxRatesUsd: %s", device_info)
        return device_info


class BnrFxRatesChf(CoordinatorEntity, SensorEntity):
    """Clasa senzorului pentru rata CHF (FX Rates - Cash)."""

    def __init__(self, coordinator):
        """Inițializează senzorul."""
        super().__init__(coordinator)
        self._attr_name = "Schimb valutar RON / CHF"
        self._attr_unique_id = f"{DOMAIN}_fx_rates_cash_chf"
        self._attr_entity_id = "sensor.fx_rates_cash_chf"

        _LOGGER.debug("Senzorul BnrFxRatesChf a fost inițializat.")

    @property
    def native_value(self):
        """Returnează valoarea principală a senzorului."""
        json_data = self.coordinator.data
        valoare = float(json_data.get("pageProps", {}).get("fxRates", {}).get("cash", {}).get("chf", {}).get("sell", 0))
        _LOGGER.debug("Valoarea principală a senzorului BnrFxRatesChf este: %.4f", valoare)
        return valoare

    @property
    def extra_state_attributes(self):
        """Returnează atributele suplimentare."""
        data = self.coordinator.data.get("pageProps", {}).get("fxRates", {}).get("cash", {}).get("chf", {})
        if not data:
            _LOGGER.debug("Nu există date pentru atributele senzorului BnrFxRatesChf.")
            return {}

        attributes = {
            "Vânzare": "%.4f" % float(data.get("sell", 0)),
            "Cumpărare": "%.4f" % float(data.get("buy", 0)),
            ATTR_ATTRIBUTION: "Date furnizate de BNR prin www.finradar.ro",
        }
        _LOGGER.debug("Atributele senzorului BnrFxRatesChf: %s", attributes)
        return attributes

    @property
    def unique_id(self):
        """Returnează identificatorul unic al senzorului."""
        return self._attr_unique_id

    @property
    def entity_id(self):
        """Returnează identificatorul explicit al entității."""
        return self._attr_entity_id

    @entity_id.setter
    def entity_id(self, value):
        """Setează identificatorul explicit al entității."""
        self._attr_entity_id = value
        _LOGGER.debug("Entity ID pentru senzorul BnrFxRatesChf a fost setat la: %s", value)

    @property
    def icon(self):
        """Pictograma senzorului."""
        return "mdi:cash"

    @property
    def device_info(self):
        """Informații despre dispozitiv pentru integrarea Schimb Valutar."""
        device_info = {
            "identifiers": {(DOMAIN, "schimbbnr")},
            "name": "Schimb valutar BNR",
            "manufacturer": "Ciprian Nicolae (cnecrea)",
            "model": "Schimb valutar BNR",
            "entry_type": DeviceEntryType.SERVICE,
        }
        _LOGGER.debug("Informațiile dispozitivului pentru BnrFxRatesChf: %s", device_info)
        return device_info


class BnrFxRatesGbp(CoordinatorEntity, SensorEntity):
    """Clasa senzorului pentru rata GBP (FX Rates - Cash)."""

    def __init__(self, coordinator):
        """Inițializează senzorul."""
        super().__init__(coordinator)
        self._attr_name = "Schimb valutar RON / GBP"
        self._attr_unique_id = f"{DOMAIN}_fx_rates_cash_gbp"
        self._attr_entity_id = "sensor.fx_rates_cash_gbp"

        _LOGGER.debug("Senzorul BnrFxRatesGbp a fost inițializat.")

    @property
    def native_value(self):
        """Returnează valoarea principală a senzorului."""
        json_data = self.coordinator.data
        valoare = float(json_data.get("pageProps", {}).get("fxRates", {}).get("cash", {}).get("gbp", {}).get("sell", 0))
        _LOGGER.debug("Valoarea principală a senzorului BnrFxRatesGbp este: %.4f", valoare)
        return valoare

    @property
    def extra_state_attributes(self):
        """Returnează atributele suplimentare."""
        data = self.coordinator.data.get("pageProps", {}).get("fxRates", {}).get("cash", {}).get("gbp", {})
        if not data:
            _LOGGER.debug("Nu există date pentru atributele senzorului BnrFxRatesGbp.")
            return {}

        attributes = {
            "Vânzare": "%.4f" % float(data.get("sell", 0)),
            "Cumpărare": "%.4f" % float(data.get("buy", 0)),
            ATTR_ATTRIBUTION: "Date furnizate de BNR prin www.finradar.ro",
        }
        _LOGGER.debug("Atributele senzorului BnrFxRatesGbp: %s", attributes)
        return attributes

    @property
    def unique_id(self):
        """Returnează identificatorul unic al senzorului."""
        return self._attr_unique_id

    @property
    def entity_id(self):
        """Returnează identificatorul explicit al entității."""
        return self._attr_entity_id

    @entity_id.setter
    def entity_id(self, value):
        """Setează identificatorul explicit al entității."""
        self._attr_entity_id = value
        _LOGGER.debug("Entity ID pentru senzorul BnrFxRatesGbp a fost setat la: %s", value)

    @property
    def icon(self):
        """Pictograma senzorului."""
        return "mdi:currency-gbp"

    @property
    def device_info(self):
        """Informații despre dispozitiv pentru integrarea Schimb Valutar."""
        device_info = {
            "identifiers": {(DOMAIN, "schimbbnr")},
            "name": "Schimb valutar BNR",
            "manufacturer": "Ciprian Nicolae (cnecrea)",
            "model": "Schimb valutar BNR",
            "entry_type": DeviceEntryType.SERVICE,
        }
        _LOGGER.debug("Informațiile dispozitivului pentru BnrFxRatesGbp: %s", device_info)
        return device_info


class DobandaRobor(CoordinatorEntity, SensorEntity):
    """Clasa senzorului pentru dobânda ROBOR."""

    def __init__(self, coordinator):
        """Inițializează senzorul."""
        super().__init__(coordinator)
        self._attr_name = "Dobânda ROBOR"
        self._attr_unique_id = f"{DOMAIN}_dobanda_robor"
        self._attr_entity_id = "sensor.dobanda_robor"

        _LOGGER.debug("Senzorul DobandaRobor a fost inițializat.")

    @property
    def native_value(self):
        """Returnează valoarea principală a senzorului (numărul de perioade ROBOR)."""
        json_data = self.coordinator.data
        robor_data = json_data.get("pageProps", {}).get("moneyRates", {}).get("robor", {})

        # Numără câte perioade există în datele JSON
        numar_perioade = sum(1 for key in ["m1", "m3", "m6", "m12"] if key in robor_data and "rate" in robor_data[key])
        _LOGGER.debug("Valoarea principală (native_value) a senzorului DobandaRobor este: %d", numar_perioade)
        return numar_perioade

    @property
    def extra_state_attributes(self):
        """Returnează atributele suplimentare."""
        robor_data = self.coordinator.data.get("pageProps", {}).get("moneyRates", {}).get("robor", {})
        if not robor_data:
            _LOGGER.debug("Nu există date pentru atributele senzorului DobandaRobor.")
            return {}

        attributes = {
            "1 lună": "%.2f" % float(robor_data.get("m1", {}).get("rate", 0)),
            "3 luni": "%.2f" % float(robor_data.get("m3", {}).get("rate", 0)),
            "6 luni": "%.2f" % float(robor_data.get("m6", {}).get("rate", 0)),
            "12 luni": "%.2f" % float(robor_data.get("m12", {}).get("rate", 0)),
            ATTR_ATTRIBUTION: "Date furnizate de BNR prin www.finradar.ro",
        }
        _LOGGER.debug("Atributele senzorului DobandaRobor (formatate cu 2 zecimale): %s", attributes)
        return attributes

    @property
    def unique_id(self):
        """Returnează identificatorul unic al senzorului."""
        return self._attr_unique_id

    @property
    def entity_id(self):
        """Returnează identificatorul explicit al entității."""
        return self._attr_entity_id

    @entity_id.setter
    def entity_id(self, value):
        """Setează identificatorul explicit al entității."""
        self._attr_entity_id = value
        _LOGGER.debug("Entity ID pentru senzorul DobandaRobor a fost setat la: %s", value)

    @property
    def icon(self):
        """Pictograma senzorului."""
        return "mdi:percent"

    @property
    def device_info(self):
        """Informații despre dispozitiv pentru integrarea Dobânda ROBOR."""
        device_info = {
            "identifiers": {(DOMAIN, "dobandarobor")},
            "name": "Dobândă ROBOR",
            "manufacturer": "Ciprian Nicolae (cnecrea)",
            "model": "Dobândă ROBOR",
            "entry_type": DeviceEntryType.SERVICE,
        }
        _LOGGER.debug("Informațiile dispozitivului pentru DobandaRobor: %s", device_info)
        return device_info


class DobandaEuribor(CoordinatorEntity, SensorEntity):
    """Clasa senzorului pentru dobânda EURIBOR."""

    def __init__(self, coordinator):
        """Inițializează senzorul."""
        super().__init__(coordinator)
        self._attr_name = "Dobânda EURIBOR"
        self._attr_unique_id = f"{DOMAIN}_dobanda_euribor"
        self._attr_entity_id = "sensor.dobanda_euribor"

        _LOGGER.debug("Senzorul DobandaEuribor a fost inițializat.")

    @property
    def native_value(self):
        """Returnează valoarea principală a senzorului (numărul de perioade EURIBOR)."""
        json_data = self.coordinator.data
        euribor_data = json_data.get("pageProps", {}).get("moneyRates", {}).get("euribor", {})

        # Numără câte perioade există în datele JSON
        numar_perioade = sum(1 for key in ["m1", "m3", "m6", "m12"] if key in euribor_data and "rate" in euribor_data[key])

        _LOGGER.debug("Valoarea principală (native_value) a senzorului DobandaEuribor este: %d", numar_perioade)
        return numar_perioade

    @property
    def extra_state_attributes(self):
        """Returnează atributele suplimentare."""
        euribor_data = self.coordinator.data.get("pageProps", {}).get("moneyRates", {}).get("euribor", {})
        if not euribor_data:
            _LOGGER.debug("Nu există date pentru atributele senzorului DobandaEuribor.")
            return {}

        attributes = {
            "1 lună": "%.2f" % float(euribor_data.get("m1", {}).get("rate", 0)),
            "3 luni": "%.2f" % float(euribor_data.get("m3", {}).get("rate", 0)),
            "6 luni": "%.2f" % float(euribor_data.get("m6", {}).get("rate", 0)),
            "12 luni": "%.2f" % float(euribor_data.get("m12", {}).get("rate", 0)),
            ATTR_ATTRIBUTION: "Date furnizate de BNR prin www.finradar.ro",
        }
        _LOGGER.debug("Atributele senzorului DobandaEuribor (formatate cu 2 zecimale): %s", attributes)
        return attributes

    @property
    def unique_id(self):
        """Returnează identificatorul unic al senzorului."""
        return self._attr_unique_id

    @property
    def entity_id(self):
        """Returnează identificatorul explicit al entității."""
        return self._attr_entity_id

    @entity_id.setter
    def entity_id(self, value):
        """Setează identificatorul explicit al entității."""
        self._attr_entity_id = value
        _LOGGER.debug("Entity ID pentru senzorul DobandaEuribor a fost setat la: %s", value)

    @property
    def icon(self):
        """Pictograma senzorului."""
        return "mdi:percent"

    @property
    def device_info(self):
        """Informații despre dispozitiv pentru integrarea Dobânda EURIBOR."""
        device_info = {
            "identifiers": {(DOMAIN, "dobandaeurobor")},
            "name": "Dobândă EURIBOR",
            "manufacturer": "Ciprian Nicolae (cnecrea)",
            "model": "Dobândă EURIBOR",
            "entry_type": DeviceEntryType.SERVICE,
        }
        _LOGGER.debug("Informațiile dispozitivului pentru DobandaEuribor: %s", device_info)
        return device_info


class IRCCzilnic(CoordinatorEntity, SensorEntity):
    """Clasa senzorului pentru IRCC zilnic."""

    def __init__(self, coordinator):
        """Inițializează senzorul."""
        super().__init__(coordinator)
        self._attr_name = "IRCC zilnic"
        self._attr_unique_id = f"{DOMAIN}_ircc_zilnic"
        self._attr_entity_id = "sensor.ircc_zilnic"

        _LOGGER.debug("Senzorul IRCCzilnic a fost inițializat.")

    @property
    def native_value(self):
        """Returnează valoarea principală a senzorului (rate)."""
        json_data = self.coordinator.data
        ircc_data = json_data.get("pageProps", {}).get("moneyRates", {}).get("irccDaily", {})
        valoare = float(ircc_data.get("rate", 0))
        _LOGGER.debug("Valoarea principală (native_value - rate) a senzorului IRCCzilnic este: %.2f", valoare)
        return valoare

    @property
    def extra_state_attributes(self):
        """Returnează atributele suplimentare."""
        ircc_data = self.coordinator.data.get("pageProps", {}).get("moneyRates", {}).get("irccDaily", {})
        if not ircc_data:
            _LOGGER.debug("Nu există date pentru atributele senzorului IRCCzilnic.")
            return {}

        attributes = {
            "Modificare": "%.2f" % float(ircc_data.get("change", 0)),
            ATTR_ATTRIBUTION: "Date furnizate de BNR prin www.finradar.ro",
        }
        _LOGGER.debug("Atributele senzorului IRCCzilnic (formatate cu 2 zecimale): %s", attributes)
        return attributes

    @property
    def unique_id(self):
        """Returnează identificatorul unic al senzorului."""
        return self._attr_unique_id

    @property
    def entity_id(self):
        """Returnează identificatorul explicit al entității."""
        return self._attr_entity_id

    @entity_id.setter
    def entity_id(self, value):
        """Setează identificatorul explicit al entității."""
        self._attr_entity_id = value
        _LOGGER.debug("Entity ID pentru senzorul IRCCzilnic a fost setat la: %s", value)

    @property
    def icon(self):
        """Pictograma senzorului."""
        return "mdi:calendar-clock"

    @property
    def device_info(self):
        """Informații despre dispozitiv pentru integrarea IRCC zilnic."""
        device_info = {
            "identifiers": {(DOMAIN, "ircc")},
            "name": "Indicele de referință pentru creditele consumatorilor",
            "manufacturer": "Ciprian Nicolae (cnecrea)",
            "model": "IIndicele de referință pentru creditele consumatorilor",
            "entry_type": DeviceEntryType.SERVICE,
        }
        _LOGGER.debug("Informațiile dispozitivului pentru IRCCzilnic: %s", device_info)
        return device_info


class IRCCTrimestrial(CoordinatorEntity, SensorEntity):
    """Clasa senzorului pentru IRCC Trimestrial."""

    def __init__(self, coordinator):
        """Inițializează senzorul."""
        super().__init__(coordinator)
        self._attr_name = "IRCC trimestrial"
        self._attr_unique_id = f"{DOMAIN}_ircc_trimestrial"
        self._attr_entity_id = "sensor.ircc_trimestrial"

        _LOGGER.debug("Senzorul IRCCTrimestrial a fost inițializat.")

    @property
    def native_value(self):
        """Returnează valoarea principală a senzorului (rate)."""
        json_data = self.coordinator.data
        ircc_data = json_data.get("pageProps", {}).get("moneyRates", {}).get("ircc", {})
        valoare = float(ircc_data.get("rate", 0))
        _LOGGER.debug("Valoarea principală (native_value - rate) a senzorului IRCCTrimestrial este: %.2f", valoare)
        return valoare

    @property
    def extra_state_attributes(self):
        """Returnează atributele suplimentare."""
        ircc_data = self.coordinator.data.get("pageProps", {}).get("moneyRates", {}).get("ircc", {})
        if not ircc_data:
            _LOGGER.debug("Nu există date pentru atributele senzorului IRCCTrimestrial.")
            return {}

        attributes = {
            "Modificare": "%.2f" % float(ircc_data.get("change", 0)),
            ATTR_ATTRIBUTION: "Date furnizate de BNR prin www.finradar.ro",
        }
        _LOGGER.debug("Atributele senzorului IRCCTrimestrial (formatate cu 2 zecimale): %s", attributes)
        return attributes

    @property
    def unique_id(self):
        """Returnează identificatorul unic al senzorului."""
        return self._attr_unique_id

    @property
    def entity_id(self):
        """Returnează identificatorul explicit al entității."""
        return self._attr_entity_id

    @entity_id.setter
    def entity_id(self, value):
        """Setează identificatorul explicit al entității."""
        self._attr_entity_id = value
        _LOGGER.debug("Entity ID pentru senzorul IRCCTrimestrial a fost setat la: %s", value)

    @property
    def icon(self):
        """Pictograma senzorului."""
        return "mdi:calendar-month"

    @property
    def device_info(self):
        """Informații despre dispozitiv pentru integrarea IRCC."""
        device_info = {
            "identifiers": {(DOMAIN, "ircc")},
            "name": "Indicele de referință pentru creditele consumatorilor",
            "manufacturer": "Ciprian Nicolae (cnecrea)",
            "model": "Indicele de referință pentru creditele consumatorilor",
            "entry_type": DeviceEntryType.SERVICE,
        }
        _LOGGER.debug("Informațiile dispozitivului pentru IRCCTrimestrial: %s", device_info)
        return device_info
