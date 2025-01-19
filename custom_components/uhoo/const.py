from datetime import timedelta
import logging

from homeassistant.const import (  # noqa:F401
    ATTR_DEVICE_CLASS,
    ATTR_ICON,
    ATTR_UNIT_OF_MEASUREMENT,
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    CONCENTRATION_PARTS_PER_BILLION,
    CONCENTRATION_PARTS_PER_MILLION,
    UnitOfPressure,
    UnitOfTemperature,
    PERCENTAGE,
)
from homeassistant.components.sensor import (
    SensorDeviceClass,
)

# Base component constants
NAME = "uHoo Integration"
MODEL = "uHoo Indoor Air Monitor"
MANUFACTURER = "uHoo"
DOMAIN = "uhoo"
VERSION = "0.0.4"
ISSUE_URL = "https://github.com/csacca/uhoo-homeassistant/issues"

# Platforms
SENSOR = "sensor"
PLATFORMS = [SENSOR]

API_CO = "co"
API_CO2 = "co2"
API_DUST = "dust"
API_HUMIDITY = "humidity"
API_NO2 = "no2"
API_OZONE = "ozone"
API_PRESSURE = "pressure"
API_TEMP = "temp"
API_VOC = "voc"

ATTR_LABEL = "label"
ATTR_UNIQUE_ID = "unique_id"


LOGGER = logging.getLogger(__package__)

UPDATE_INTERVAL = timedelta(seconds=60)

SENSOR_TYPES = {
    API_CO: {
        ATTR_DEVICE_CLASS: SensorDeviceClass.CO,
        ATTR_ICON: "mdi:molecule-co",
        ATTR_UNIT_OF_MEASUREMENT: CONCENTRATION_PARTS_PER_MILLION,
        ATTR_LABEL: "Carbon monoxide",
        ATTR_UNIQUE_ID: API_CO,
    },
    API_CO2: {
        ATTR_DEVICE_CLASS: SensorDeviceClass.CO2,
        ATTR_ICON: "mdi:molecule-co2",
        ATTR_UNIT_OF_MEASUREMENT: CONCENTRATION_PARTS_PER_MILLION,
        ATTR_LABEL: "Carbon dioxide",
        ATTR_UNIQUE_ID: API_CO2,
    },
    API_DUST: {
        ATTR_DEVICE_CLASS: None,  # DEVICE_CLASS_PM25 once 2021.9 is out
        ATTR_ICON: "mdi:blur",
        ATTR_UNIT_OF_MEASUREMENT: CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        ATTR_LABEL: "PM2.5",
        ATTR_UNIQUE_ID: API_DUST,
    },
    API_HUMIDITY: {
        ATTR_DEVICE_CLASS: SensorDeviceClass.HUMIDITY,
        ATTR_ICON: "mdi:water-percent",
        ATTR_UNIT_OF_MEASUREMENT: PERCENTAGE,
        ATTR_LABEL: "Humidity",
        ATTR_UNIQUE_ID: API_HUMIDITY,
    },
    API_NO2: {
        ATTR_DEVICE_CLASS: None,  # DEVICE_CLASS_NITROGEN_DIOXIDE once 2021.9 is out
        ATTR_ICON: "mdi:cloud",
        ATTR_UNIT_OF_MEASUREMENT: CONCENTRATION_PARTS_PER_BILLION,
        ATTR_LABEL: "Nitrogen dioxide",
        ATTR_UNIQUE_ID: API_NO2,
    },
    API_OZONE: {
        ATTR_DEVICE_CLASS: None,  # DEVICE_CLASS_OZONE once 2021.9 is out
        ATTR_ICON: "mdi:cloud",
        ATTR_UNIT_OF_MEASUREMENT: CONCENTRATION_PARTS_PER_BILLION,
        ATTR_LABEL: "Ozone",
        ATTR_UNIQUE_ID: API_OZONE,
    },
    API_PRESSURE: {
        ATTR_DEVICE_CLASS: SensorDeviceClass.PRESSURE,
        ATTR_ICON: "mdi:gauge",
        ATTR_UNIT_OF_MEASUREMENT: UnitOfPressure.HPA,
        ATTR_LABEL: "Air pressure",
        ATTR_UNIQUE_ID: API_PRESSURE,
    },
    API_TEMP: {
        ATTR_DEVICE_CLASS: SensorDeviceClass.TEMPERATURE,
        ATTR_ICON: "mdi:thermometer",
        ATTR_UNIT_OF_MEASUREMENT: UnitOfTemperature.FAHRENHEIT,
        ATTR_LABEL: "Temperature",
        ATTR_UNIQUE_ID: API_TEMP,
    },
    API_VOC: {
        ATTR_DEVICE_CLASS: None,  # DEVICE_CLASS_VOLATILE_ORGANIC_COMPOUNDS once 2021.9 is out
        ATTR_ICON: "mdi:cloud",
        ATTR_UNIT_OF_MEASUREMENT: CONCENTRATION_PARTS_PER_BILLION,
        ATTR_LABEL: "Total volatile organic compounds",
        ATTR_UNIQUE_ID: API_VOC,
    },
}


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
