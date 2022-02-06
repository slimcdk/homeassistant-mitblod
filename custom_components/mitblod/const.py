"""Constants for the MitBlod integration."""
from __future__ import annotations

from typing import Final

import logging
import pymitblod
from datetime import timedelta

import voluptuous as vol

from homeassistant.const import (
    CONF_NAME, 
    CONF_PASSWORD
)

DOMAIN: Final = "mitblod"

CONF_IDENTIFICATION: Final = "identification"
CONF_INSTITUTION: Final = "institution"
CONF_BIRTHDAY: Final = "birthday"
CONF_WEIGHT: Final = "weight"
CONF_HEIGHT: Final = "height"
CONF_GENDER: Final = "gender"


def validate_datetime(val):
    print(val)
    return val

MITBLOD_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME): str,
        vol.Required(CONF_IDENTIFICATION): str,
        vol.Required(CONF_PASSWORD): str,
        vol.Required(CONF_INSTITUTION, default=str(pymitblod.Institutions.list()[0])): vol.In([str(i) for i in pymitblod.Institutions.list()]),
        vol.Required(CONF_HEIGHT): int,
        vol.Required(CONF_WEIGHT): int,
        vol.Required(CONF_BIRTHDAY): str, # vol.datetime,
        vol.Required(CONF_GENDER, default=str(pymitblod.Genders.list()[0])): vol.In([str(g) for g in pymitblod.Genders.list()])
    }
)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema({})
    }, 
    extra=vol.ALLOW_EXTRA
)


_LOGGER = logging.getLogger(__name__)
