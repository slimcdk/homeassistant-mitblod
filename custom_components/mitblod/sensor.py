
from __future__ import annotations

import pymitblod

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.typing import StateType
from homeassistant.const import (
    STATE_UNAVAILABLE,
    STATE_UNKNOWN
)

from .const import (
    DOMAIN,

    _LOGGER
)

async def async_setup_entry(hass, config, async_add_entities):
    """Set up the sensor platform."""
    patient = hass.data[DOMAIN][config.entry_id]

    async_add_entities([
        MitBlodDonations(patient=patient),
        MitBlodMessages(patient=patient),
        MitBlodNextBooking(patient=patient),
        MitBlodBlood(patient=patient)
    ])



class MitBlodDonations(Entity):
    """Representation of a Sensor."""

    def __init__(self, patient:pymitblod.MitBlod):
        """Initialize the sensor."""
        self._patient = patient
        self._attr_name = f"{self._patient.name()}s donations"
        self.entity_id = f"sensor.{'_'.join([DOMAIN, self._attr_name]).replace(' ', '_').lower()}"
        self._attr_unique_id = f"{self.entity_id}_{self._patient.partial_id()}"
        self._attr_state_attributes = None

    @property
    def state_attributes(self) -> dict[str, Any] | None:
        """Return state attributes."""       
        return self._attr_state_attributes

    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        donations = self._patient.donations()
        self._attr_state = len(donations)
        self._attr_state_attributes = dict(history=donations)


class MitBlodMessages(Entity):
    """Representation of a Sensor."""

    def __init__(self, patient:pymitblod.MitBlod):
        """Initialize the sensor."""
        self._patient = patient
        self._attr_name = f"{self._patient.name()}s messages"
        self.entity_id = f"sensor.{'_'.join([DOMAIN, self._attr_name]).replace(' ', '_').lower()}"
        self._attr_unique_id = f"{self.entity_id}_{self._patient.partial_id()}"
        self._attr_state_attributes = None

    @property
    def state_attributes(self) -> dict[str, Any] | None:
        """Return state attributes."""       
        return self._attr_state_attributes

    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        messages = self._patient.messages()
        self._attr_state = len(messages)
        self._attr_state_attributes = dict(history=messages[:10])



class MitBlodNextBooking(Entity):
    """Representation of a Sensor."""

    def __init__(self, patient:pymitblod.MitBlod):
        """Initialize the sensor."""
        self._patient = patient
        self._attr_name = f"{self._patient.name()}s next booking"
        self.entity_id = f"sensor.{'_'.join([DOMAIN, self._attr_name]).replace(' ', '_').lower()}"
        self._attr_unique_id = f"{self.entity_id}_{self._patient.partial_id()}"
        self._attr_state_attributes = None

    @property
    def state_attributes(self) -> dict[str, Any] | None:
        """Return state attributes."""
        return self._attr_state_attributes

    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        bookings = self._patient.next_bookings()
        if len(bookings) > 0:
            self._attr_state = bookings[0]["date"]
            self._attr_state_attributes = bookings[0]
        else:
            self._attr_state = STATE_UNKNOWN
            self._attr_state_attributes = dict()



class MitBlodBlood(Entity):
    """Representation of a Sensor."""

    def __init__(self, patient:pymitblod.MitBlod):
        """Initialize the sensor."""
        self._patient = patient
        self._attr_name = f"{self._patient.name()}s blood"
        self.entity_id = f"sensor.{'_'.join([DOMAIN, self._attr_name]).replace(' ', '_').lower()}"
        self._attr_unique_id = f"{self.entity_id}_{self._patient.partial_id()}"
        self._attr_state_attributes = None

    @property
    def state_attributes(self) -> dict[str, Any] | None:
        """Return state attributes."""
        return self._attr_state_attributes

    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        blood_type = self._patient.blood_type()
        self._attr_state = blood_type
        self._attr_state_attributes = dict(
            blood_type = blood_type,
            blood_volume_ml = int(self._patient.blood_volume_ml())
        )
