"""Config flow for MitBlod integration."""
import pymitblod

from datetime import datetime

from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.typing import ConfigType
from homeassistant.config_entries import ConfigFlow, CONN_CLASS_CLOUD_POLL
from homeassistant.const import (
    CONF_NAME, 
    CONF_PASSWORD
)

from .const import (
    CONF_BIRTHDAY,
    CONF_HEIGHT,
    CONF_WEIGHT,
    CONF_GENDER,
    CONF_IDENTIFICATION,
    CONF_INSTITUTION,
    DOMAIN,

    MITBLOD_SCHEMA,

    _LOGGER
)

async def create_client(hass:HomeAssistant, user_input:dict):

    patient = pymitblod.MitBlod(
        identification=user_input[CONF_IDENTIFICATION],
        password=user_input[CONF_PASSWORD],
        institution=pymitblod.Institutions.get_enum_for(value=user_input[CONF_INSTITUTION]),
        name=user_input[CONF_NAME],
        birthday=datetime.strptime(str(user_input[CONF_BIRTHDAY]), "%d-%m-%Y %H:%M"),
        weight=user_input[CONF_WEIGHT],
        height=user_input[CONF_HEIGHT],
        gender=pymitblod.Genders.get_enum_for(value=user_input[CONF_GENDER])
    )
    return hass.async_add_executor_job(patient.can_login)


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
            if await create_client(hass=self.hass, user_input=user_input):
                self._init_data = user_input
                return await self.async_step_finish()
        return self.async_show_form(step_id="user", data_schema=MITBLOD_SCHEMA, errors=errors)
    

    async def async_step_finish(self) -> FlowResult:
        data = {**self._init_data, **self._additional_data}
        name = data[CONF_NAME] # if CONF_NAME in self._additional_data else get_mitblod_name(self.hass, self._init_data)
        return self.async_create_entry(title=f"{name} at {data[CONF_INSTITUTION]}", data=data)