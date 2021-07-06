"""The MitBlod integration."""
import asyncio
from datetime import timedelta

import pymitblod

import voluptuous as vol

from homeassistant.util import Throttle
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import (
    CONF_NAME, 
    CONF_PASSWORD
)

from .const import (
    CONF_AGE,
    CONF_HEIGHT,
    CONF_IDENTIFICATION,
    CONF_INSTITUTION,
    CONF_SEX,
    CONF_WEIGHT,
    DOMAIN,

    CONFIG_SCHEMA as _CONFIG_SCHEMA,

    _LOGGER
)


CONFIG_SCHEMA = _CONFIG_SCHEMA

PLATFORMS = ["sensor"]

MIN_TIME_BETWEEN_UPDATES = timedelta(hours=12)



async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the MitBlod component."""
    hass.data[DOMAIN] = {}
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up MitBlod from a config entry."""

    institution_enum = pymitblod.Institutions.get_enum_with(value=entry.data[CONF_INSTITUTION])
    gender_enum = pymitblod.Genders.get_enum_with(value=entry.data[CONF_SEX])

    hass.data[DOMAIN][entry.entry_id] = pymitblod.MitBlod(
        identification=entry.data[CONF_IDENTIFICATION],
        password=entry.data[CONF_PASSWORD],
        institution=institution_enum,
        name=entry.data[CONF_NAME],
        age=entry.data[CONF_AGE],
        weight=entry.data[CONF_WEIGHT],
        height=entry.data[CONF_HEIGHT],
        gender=gender_enum
    )

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