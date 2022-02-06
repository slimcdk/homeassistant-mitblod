from __future__ import annotations

import pymitblod

from datetime import timedelta

from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator
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
        MitBlodHealth(patient=patient),
        MitBlodDonations(patient=patient),
        MitBlodMessages(patient=patient),
        MitBlodNextBooking(patient=patient)
    ])


class MitBlodHealth(Entity): #(CoordinatorEntity):
    """Representation of a Sensor."""

    def __init__(self, patient:pymitblod.MitBlod):
        """Initialize the sensor."""
        self._patient = patient
        self._attr_name = "{}s health".format(self._patient.name())
        self.entity_id = "sensor.{}_{}".format(DOMAIN, self._attr_name).replace(' ', '_').lower()
        self._attr_unique_id = "{}_{}".format(self.entity_id, self._patient.partial_id())
        self._attr_state_attributes = None
        self._attr_context_recent_time = timedelta(hours=6)
        self.coordinator = DataUpdateCoordinator(
            name = "{} update coordinator".format(self._attr_name),
            hass = self.hass,
            update_interval = timedelta(hours=6),
            update_method = self.update,
            logger = _LOGGER
        )
        self._attr_force_update = True


    @property
    def state_attributes(self) -> dict[str, Any] | None:
        """Return state attributes."""       
        return self._attr_state_attributes

    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """

        self._attr_state = self._patient.mitblod_name()
        self._attr_state_attributes = dict(
            blood_type = self._patient.blood_type(),
            estimated_blood_volume = self._patient.estimated_blood_volume_ml(),
            nadlers_estimated_blood_volume = self._patient.estimated_blood_volume_ml(method="nadlers"),
            lemmens_estimated_blood_volume = self._patient.estimated_blood_volume_ml(method="lemmens"),
            
            body_mass_index = self._patient.body_mass_index(),
            body_mass_index_class = self._patient.body_mass_index_class(),

            gender = str(self._patient.gender()),
            age = self._patient.age(),
            age_friendly = str(timedelta(days=self._patient.age()*365.25)),
            weight = self._patient.weight(),
            height = self._patient.height(),

            institution = str(self._patient.institution()),
        )


class MitBlodDonations(Entity): #(CoordinatorEntity):
    """Representation of a Sensor."""

    def __init__(self, patient:pymitblod.MitBlod):
        """Initialize the sensor."""
        self._patient = patient
        self._attr_name = "{}s donations".format(self._patient.name())
        self.entity_id = "sensor.{}_{}".format(DOMAIN, self._attr_name).replace(' ', '_').lower()
        self._attr_unique_id = "{}_{}".format(self.entity_id, self._patient.partial_id())
        self._attr_state_attributes = None
        self._attr_context_recent_time = timedelta(hours=2)
        self.coordinator = DataUpdateCoordinator(
            name = "{} update coordinator".format(self._attr_name),
            hass = self.hass,
            update_interval = timedelta(hours=2),
            update_method = self.update,
            logger = _LOGGER
        )
        self._attr_force_update = True


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
        self._attr_state_attributes = dict(
            previous_donation_date=donations[0]["donationDate"],
            previous_donation_date_iso8601=donations[0]["donationDateISO8601"],
            previous_donation_hb=donations[0]["donationHB"],
            previous_donation_bp=donations[0]["donationBP"],
            previous_donation_ferritin=donations[0]["donationFerritin"],
            previous_donation_pulse=donations[0]["donationPulse"],
            previous_donation_type=donations[0]["donationType"],
            history=donations
        )


class MitBlodMessages(Entity): #(CoordinatorEntity):
    """Representation of a Sensor."""

    def __init__(self, patient:pymitblod.MitBlod):
        """Initialize the sensor."""
        self._patient = patient
        self._attr_name = "{}s messages".format(self._patient.name())
        self.entity_id = "sensor.{}_{}".format(DOMAIN, self._attr_name).replace(' ', '_').lower()
        self._attr_unique_id = "{}_{}".format(self.entity_id, self._patient.partial_id())
        self._attr_state_attributes = None
        self._attr_context_recent_time = timedelta(minutes=30)
        self.coordinator = DataUpdateCoordinator(
            name = "{} update coordinator".format(self._attr_name),
            hass = self.hass,
            update_interval = timedelta(minutes=30),
            update_method = self.update,
            logger = _LOGGER
        )
        self._attr_force_update = True


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



class MitBlodNextBooking(Entity): #(CoordinatorEntity):
    """Representation of a Sensor."""

    def __init__(self, patient:pymitblod.MitBlod):
        """Initialize the sensor."""
        self._patient = patient
        self._attr_name = "{}s next appointment".format(self._patient.name())
        self.entity_id = "sensor.{}_{}".format(DOMAIN, self._attr_name).replace(' ', '_').lower()
        self._attr_unique_id = "{}_{}".format(self.entity_id, self._patient.partial_id())
        self._attr_state_attributes = None
        self._attr_context_recent_time = timedelta(hours=1)
        self.coordinator = DataUpdateCoordinator(
            name = "{} update coordinator".format(self._attr_name),
            hass = self.hass,
            update_interval = timedelta(hours=1),
            update_method = self.update,
            logger = _LOGGER
        )
        self._attr_force_update = True


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
            self._attr_state_attributes = dict(
                # next_location=bookings[0]["location"],
                next_location_id=bookings[0]["location"]["id"],
                next_location_region=bookings[0]["location"]["region"],
                next_location_name=bookings[0]["location"]["name"],
                next_location_area=bookings[0]["location"]["area"],
                next_donation_type=bookings[0]["type"],
                other_upcoming=bookings[1:]
            )
        else:
            self._attr_state = STATE_UNKNOWN




## https://github.com/dogmatic69/nordigen-ha-lib/blob/master/nordigen_lib/sensor.py#L70-L98
## https://github.com/dogmatic69/nordigen-ha-lib/blob/master/nordigen_lib/sensor.py#L113