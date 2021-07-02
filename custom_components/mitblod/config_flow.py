"""Config flow for MitBlod integration."""
import copy
import logging

import voluptuous as vol

from homeassistant import config_entries, core, exceptions

from .const import DOMAIN  # pylint:disable=unused-import

import pymitblod

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema({
    vol.Required("identification"): str,
    vol.Required("password"): str, 
    vol.Required("institution", default=pymitblod.Institutions.list()[0].name()): vol.In( 
        [pymitblod.Institutions.list()[0].name(), pymitblod.Institutions.list()[1].name()]
    )
})



async def your_validate_func():
    pass

async def validate_input(hass: core.HomeAssistant, data):
    """Validate the user input allows us to connect.

    Data has the keys from DATA_SCHEMA with values provided by the user.
    """
    # TODO validate the data can be used to set up a connection.

    # If your PyPI package is not built with async, pass your methods
    # to the executor:
    await hass.async_add_executor_job(
        your_validate_func, data["identification"], data["password"], data["institution"]
    )

    identification = data["identification"]
    password = data["password"]
    institution = data["institution"]
    
    # hub = PlaceholderHub(data["host"])
    # if not await hub.authenticate(identification, password):
    #     raise InvalidAuth

    # If you cannot connect:
    # throw CannotConnect
    # If the authentication is wrong:
    # InvalidAuth

    # Return info that you want to store in the config entry.
    return {"title": f"MitBlod at {institution}"}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for MitBlod."""

    VERSION = 1
    
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            try:
                #info = await validate_input(self.hass, user_input)
                identification = user_input["identification"]
                password = user_input["password"]
                institution = user_input["institution"]
                info = f"MitBlod at {institution}"
                return self.async_create_entry(title=info, data=user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(exceptions.HomeAssistantError):
    """Error to indicate there is invalid auth."""