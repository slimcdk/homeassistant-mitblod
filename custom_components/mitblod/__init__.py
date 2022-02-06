"""The MitBlod integration."""
import asyncio

import pymitblod
from datetime import datetime

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import (
    CONF_NAME, 
    CONF_PASSWORD
)

from .const import (
    CONF_BIRTHDAY,
    CONF_HEIGHT,
    CONF_IDENTIFICATION,
    CONF_INSTITUTION,
    CONF_GENDER,
    CONF_WEIGHT,
    DOMAIN,

    CONFIG_SCHEMA as _CONFIG_SCHEMA,

    _LOGGER
)


CONFIG_SCHEMA = _CONFIG_SCHEMA

PLATFORMS = ["sensor"]


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the MitBlod component."""
    hass.data[DOMAIN] = {}
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up MitBlod from a config entry."""

    patient = pymitblod.MitBlod(
        identification=entry.data[CONF_IDENTIFICATION],
        password=entry.data[CONF_PASSWORD],
        institution=pymitblod.Institutions.get_enum_for(value=entry.data[CONF_INSTITUTION]),
        name=entry.data[CONF_NAME],
        birthday=datetime.strptime(str(entry.data[CONF_BIRTHDAY]), "%d-%m-%Y %H:%M"),
        weight=entry.data[CONF_WEIGHT],
        height=entry.data[CONF_HEIGHT],
        gender=pymitblod.Genders.get_enum_for(value=entry.data[CONF_GENDER])
    )
    hass.data[DOMAIN][entry.entry_id] = patient
    
    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok