"""Test uHoo sensors."""

from datetime import timedelta
from unittest.mock import patch

from pytest_homeassistant_custom_component.common import async_fire_time_changed

from custom_components.uhoo.const import (  # noqa:F401
    API_CO,
    API_CO2,
    API_DUST,
    API_HUMIDITY,
    API_NO2,
    API_OZONE,
    API_PRESSURE,
    API_TEMP,
    API_VOC,
    ATTR_LABEL,
    SENSOR_TYPES,
)
from homeassistant.components.sensor import ATTR_STATE_CLASS, SensorStateClass
from homeassistant.const import (
    ATTR_DEVICE_CLASS,
    ATTR_ICON,
    ATTR_UNIT_OF_MEASUREMENT,
    STATE_UNAVAILABLE,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry
from homeassistant.helpers.entity_registry import EntityRegistry
from homeassistant.util.dt import utcnow

from . import setup_uhoo_config
from .const import MOCK_DEVICE, MOCK_DEVICE_DATA


def assert_expected_properties(
    hass: HomeAssistant,
    registry: EntityRegistry,
    serial_number: str,
    sensor_type: str,
):
    """Assert expected properties."""

    device_name = str(MOCK_DEVICE["name"]).lower().replace(" ", "_")
    sensor_name = (
        str(SENSOR_TYPES[sensor_type][ATTR_LABEL])
        .lower()
        .replace(" ", "_")
        .replace(".", "_")
    )

    state = hass.states.get(f"sensor.uhoo_{device_name}_{sensor_name}")

    assert state
    assert state.state == f"{str(MOCK_DEVICE_DATA[sensor_type]['value'])}"

    # Attributes
    assert state.attributes.get(ATTR_STATE_CLASS) == SensorStateClass.MEASUREMENT
    assert state.attributes.get(ATTR_ICON) == SENSOR_TYPES[sensor_type][ATTR_ICON]
    assert (
        state.attributes.get(ATTR_UNIT_OF_MEASUREMENT)
        == SENSOR_TYPES[sensor_type][ATTR_UNIT_OF_MEASUREMENT]
    )

    assert (
        state.attributes.get(ATTR_DEVICE_CLASS)
        == SENSOR_TYPES[sensor_type][ATTR_DEVICE_CLASS]
    )

    entity = registry.async_get(f"sensor.uhoo_{device_name}_{sensor_name}")

    assert entity
    assert entity.unique_id == f"{serial_number}_{sensor_type}"


async def test_sensors(
    hass: HomeAssistant, bypass_login, bypass_get_latest_data, bypass_get_devices
):
    """Test states of the sensors."""

    await setup_uhoo_config(hass)

    serial_number = MOCK_DEVICE_DATA["serialNumber"]
    registry: EntityRegistry = entity_registry.async_get(hass)

    assert_expected_properties(hass, registry, serial_number, API_CO)
    assert_expected_properties(hass, registry, serial_number, API_CO2)
    assert_expected_properties(hass, registry, serial_number, API_DUST)
    assert_expected_properties(hass, registry, serial_number, API_HUMIDITY)
    assert_expected_properties(hass, registry, serial_number, API_NO2)
    assert_expected_properties(hass, registry, serial_number, API_OZONE)
    assert_expected_properties(hass, registry, serial_number, API_PRESSURE)

    # skipping temperature for now due to conversions being complicated
    # assert_expected_properties(hass, registry, serial_number, API_TEMP)

    assert_expected_properties(hass, registry, serial_number, API_VOC)


async def test_availability(
    hass: HomeAssistant, bypass_login, bypass_get_latest_data, bypass_get_devices
):
    await setup_uhoo_config(hass)

    state = hass.states.get("sensor.uhoo_main_humidity")
    assert state
    assert state.state != STATE_UNAVAILABLE
    assert state.state == "50.7"

    with patch(
        "custom_components.uhoo.Client.get_latest_data", side_effect=ConnectionError()
    ):
        future = utcnow() + timedelta(minutes=60)
        async_fire_time_changed(hass, future)
        await hass.async_block_till_done()

        state = hass.states.get("sensor.uhoo_main_humidity")
        assert state
        assert state.state == STATE_UNAVAILABLE

    future = utcnow() + timedelta(minutes=60)
    async_fire_time_changed(hass, future)
    await hass.async_block_till_done()

    state = hass.states.get("sensor.uhoo_main_humidity")
    assert state
    assert state.state != STATE_UNAVAILABLE
    assert state.state == "50.7"
