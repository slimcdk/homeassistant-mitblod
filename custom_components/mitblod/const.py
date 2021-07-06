"""Constants for the MitBlod integration."""

import logging
import pymitblod

import voluptuous as vol

from homeassistant.const import (
    CONF_NAME, 
    CONF_PASSWORD
)

DOMAIN = "mitblod"

CONF_IDENTIFICATION = "identification"
CONF_INSTITUTION = "institution"
CONF_AGE = "age"
CONF_WEIGHT = "weight"
CONF_HEIGHT = "height"
CONF_SEX = "sex"
CONF_GENDER = "gender"
CONF_ADDITIONAL_DATA = "additional_data"


MITBLOD_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_IDENTIFICATION): str,
        vol.Required(CONF_PASSWORD): str,
        vol.Required(CONF_INSTITUTION, default=pymitblod.Institutions.list()[0]): vol.In(pymitblod.Institutions.list()),
        # vol.Required(CONF_ADDITIONAL_DATA, default=True): bool,
    }
)

USERDATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME): str,
        vol.Required(CONF_HEIGHT): int,
        vol.Required(CONF_WEIGHT): int,
        vol.Required(CONF_AGE): int,
        vol.Required(CONF_SEX, default=pymitblod.Genders.list()[0]): vol.In(pymitblod.Genders.list())
    }
)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema({})
    }, 
    extra=vol.ALLOW_EXTRA
)


_LOGGER = logging.getLogger(__name__)
