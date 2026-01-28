"""
Custom integration to integrate Solity LAVO Smart Lock with Home Assistant.

For more details about this integration, please refer to
https://github.com/hpware/solity-ha
"""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING

from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, Platform
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.loader import async_get_loaded_integration

from .api import SolityApiClient
from .const import DOMAIN, LOGGER
from .coordinator import SolityDataUpdateCoordinator
from .data import SolityData

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import SolityConfigEntry

PLATFORMS: list[Platform] = [
    Platform.LOCK,
    Platform.SENSOR,
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SolityConfigEntry,
) -> bool:
    """Set up Solity integration using UI."""
    client = SolityApiClient(
        username=entry.data[CONF_USERNAME],
        password=entry.data[CONF_PASSWORD],
        session=async_get_clientsession(hass),
    )

    # Login and get devices
    await client.async_login()
    devices = await client.async_get_devices()

    coordinator = SolityDataUpdateCoordinator(
        hass=hass,
        logger=LOGGER,
        name=DOMAIN,
        update_interval=timedelta(minutes=5),
        client=client,
        devices=devices,
    )

    entry.runtime_data = SolityData(
        client=client,
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
        devices=devices,
    )

    await coordinator.async_config_entry_first_refresh()
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: SolityConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(
    hass: HomeAssistant,
    entry: SolityConfigEntry,
) -> None:
    """Reload config entry."""
    await hass.config_entries.async_reload(entry.entry_id)
