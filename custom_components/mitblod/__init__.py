"""The MitBlod integration."""
import asyncio
import logging
import sys

import voluptuous as vol
from homeassistant.util import Throttle
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from pymitblod import MitBlod, Institutions

from .const import DOMAIN

import requests

_LOGGER = logging.getLogger(__name__)


CONFIG_SCHEMA = vol.Schema({DOMAIN: vol.Schema({})}, extra=vol.ALLOW_EXTRA)

PLATFORMS = ["sensor"]

MIN_TIME_BETWEEN_UPDATES = timedelta(hours=1)


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the MitBlod component."""
    hass.data[DOMAIN] = {}
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up MitBlod from a config entry."""
    identification = entry.data['identification']
    password = entry.data['password']
    institution = entry.data['institution']

    
    hass.data[DOMAIN][entry.entry_id] = HassMitBlod(identification, password, institution)

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

class HassMitBlod:
    def __init__(self, identification, password, institution):
        #self._client = MitBlod(identification, password, institution)
        self.institution = institution
        self._data = None
