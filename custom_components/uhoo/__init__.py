"""
Custom integration to integrate uHoo with Home Assistant.

For more details about this integration, please refer to
https://github.com/csacca/uhoo-homeassistant
"""
import asyncio
from typing import Dict, List

from pyuhoo import Client
from pyuhoo.device import Device
from pyuhoo.errors import UhooError, UnauthorizedError

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfPressure, UnitOfTemperature, CONF_PASSWORD, CONF_USERNAME
from homeassistant.core_config import Config
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, LOGGER, PLATFORMS, STARTUP_MESSAGE, UPDATE_INTERVAL

# https://github.com/home-assistant/example-custom-config/tree/master/custom_components

async def async_setup(hass: HomeAssistant, config: Config) -> bool:
    """Set up all platforms for this device/entry."""
    return True


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up uHoo integration from a config entry."""

    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        LOGGER.info(STARTUP_MESSAGE)

    # get username and password from configuration
    username = config_entry.data.get(CONF_USERNAME)
    password = config_entry.data.get(CONF_PASSWORD)

    # get aiohttp session
    session = async_get_clientsession(hass)

    # initial login
    try:
        client = Client(username, password, session)
        await client.login()
    except UnauthorizedError as err:
        LOGGER.error(f"Error: 401 Unauthorized error while logging in: {err}")
        return False
    except UhooError as err:
        raise ConfigEntryNotReady(err) from err

    # create data update coordinator
    coordinator = UhooDataUpdateCoordinator(hass, client=client)
    await coordinator.async_refresh()

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    hass.data[DOMAIN][config_entry.entry_id] = coordinator
    for platform in PLATFORMS:
        hass.async_add_job(hass.config_entries.async_forward_entry_setup(
                config_entry, platform))
   
    return True


class UhooDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the uHoo API."""

    def __init__(self, hass: HomeAssistant, client: Client) -> None:
        """Initialize."""
        self.client = client
        self.platforms: List[str] = []
        self.user_settings_temp = None

        super().__init__(hass, LOGGER, name=DOMAIN, update_interval=UPDATE_INTERVAL)

    async def _async_update_data(self) -> Dict[str, Device]:
        try:
            await self.client.get_latest_data()
            self.user_settings_temp = self.client.user_settings_temp
            return self.client.get_devices()  # type: ignore
        except Exception as exception:
            LOGGER.error(
                f"Error: an exception occurred while attempting to get latest data: {exception}"
            )
            raise UpdateFailed() from exception


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""

    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    unloaded = all(
        await asyncio.gather(
            *(
                hass.config_entries.async_forward_entry_unload(config_entry, platform)
                for platform in PLATFORMS
                if platform in coordinator.platforms
            )
        )
    )

    await hass.async_block_till_done()

    if unloaded:
        hass.data[DOMAIN].pop(config_entry.entry_id)

    return unloaded
