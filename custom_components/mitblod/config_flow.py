"""Config flow for MitBlod integration."""
import pymitblod

from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.typing import ConfigType
from homeassistant.config_entries import ConfigFlow, CONN_CLASS_CLOUD_POLL
from homeassistant.const import (
    CONF_NAME, 
    CONF_PASSWORD
)

from .const import (
    CONF_IDENTIFICATION,
    CONF_INSTITUTION,
    DOMAIN,
    CONF_ADDITIONAL_DATA,

    MITBLOD_SCHEMA,
    USERDATA_SCHEMA,

    _LOGGER
)


async def validate_login(hass:HomeAssistant, user_input:dict):
    institution_enum = pymitblod.Institutions.get_enum_with(value=user_input[CONF_INSTITUTION])
    patient = pymitblod.MitBlod(
        identification=user_input[CONF_IDENTIFICATION],
        password=user_input[CONF_PASSWORD],
        institution=institution_enum
    )
    return hass.async_add_executor_job(patient.can_login)


async def get_mitblod_name(hass:HomeAssistant, user_input:dict):
    institution_enum = pymitblod.Institutions.get_enum_with(value=user_input[CONF_INSTITUTION])
    patient = pymitblod.MitBlod(
        identification=user_input[CONF_IDENTIFICATION],
        password=user_input[CONF_PASSWORD],
        institution=institution_enum
    )
    return hass.async_add_executor_job(patient.mitblod_name)




class MitBlodFlowHandler(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for MitBlod."""

    VERSION = 1
    CONNECTION_CLASS = CONN_CLASS_CLOUD_POLL
    
    def __init__(self) -> None:
        super().__init__()
        self._init_data = {}
        self._additional_data = {}

    
    async def async_step_user(self, user_input:dict=None) -> FlowResult:
        """Handle a flow initiated by the user."""
        
        errors={}
        if user_input is not None:
            if await validate_login(hass=self.hass, user_input=user_input):
                self._init_data = user_input
                return await self.async_step_additional()
        return self.async_show_form(step_id="user", data_schema=MITBLOD_SCHEMA, errors=errors)
    

    async def async_step_additional(self, user_input:dict=None) -> FlowResult:
        errors = {}
        if user_input is not None:
            self._additional_data = user_input
            return await self.async_step_finish()
        return self.async_show_form(step_id="additional", data_schema=USERDATA_SCHEMA, errors=errors)


    async def async_step_finish(self) -> FlowResult:
        data = {**self._init_data, **self._additional_data}
        name = data[CONF_NAME] if CONF_NAME in self._additional_data else get_mitblod_name(self.hass, self._init_data)
        return self.async_create_entry(title=f"{name} at {data[CONF_INSTITUTION]}", data=data)