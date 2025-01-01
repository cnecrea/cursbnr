"""Config flow pentru integrarea Curs valutar BNR."""
import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN, DEFAULT_UPDATE_INTERVAL, MIN_UPDATE_INTERVAL, MAX_UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)

class CursBnrConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow pentru integrarea Curs valutar BNR."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Pasul inițial de configurare."""
        _LOGGER.debug("Pasul inițial de configurare a fost apelat.")
        
        if user_input is not None:
            _LOGGER.debug(
                "Datele introduse de utilizator în timpul configurării: %s", user_input
            )
            # Creează entry-ul și salvează datele introduse
            return self.async_create_entry(
                title="Curs valutar BNR",
                data={
                    "update_interval": user_input["update_interval"],
                },
            )

        _LOGGER.debug(
            "Afișăm formularul pentru configurare. Interval implicit de actualizare: %s secunde",
            DEFAULT_UPDATE_INTERVAL,
        )

        # Schema pentru formularul de configurare
        data_schema = vol.Schema(
            {
                vol.Required(
                    "update_interval",
                    default=DEFAULT_UPDATE_INTERVAL,
                ): vol.All(vol.Coerce(int), vol.Range(min=MIN_UPDATE_INTERVAL, max=MAX_UPDATE_INTERVAL)),
            }
        )

        return self.async_show_form(step_id="user", data_schema=data_schema)


class CursBnrOptionsFlow(config_entries.OptionsFlow):
    """Options flow pentru integrarea Curs valutar BNR."""

    async def async_step_init(self, user_input=None):
        """Pasul de configurare a opțiunilor."""
        _LOGGER.debug("Pasul de configurare a opțiunilor a fost apelat.")

        if user_input is not None:
            _LOGGER.debug(
                "Opțiunile actualizate de utilizator: %s", user_input
            )
            # Actualizează opțiunile
            return self.async_create_entry(title="", data=user_input)

        # Preia opțiunile salvate
        current_interval = self.options.get("update_interval", DEFAULT_UPDATE_INTERVAL)
        _LOGGER.debug(
            "Opțiunile curente pentru intervalul de actualizare: %s secunde",
            current_interval,
        )

        # Schema pentru formularul de opțiuni
        options_schema = vol.Schema(
            {
                vol.Required(
                    "update_interval",
                    default=current_interval,
                ): vol.All(vol.Coerce(int), vol.Range(min=MIN_UPDATE_INTERVAL, max=MAX_UPDATE_INTERVAL)),
            }
        )

        return self.async_show_form(step_id="init", data_schema=options_schema)