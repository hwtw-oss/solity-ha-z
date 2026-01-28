"""DataUpdateCoordinator for Solity integration."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import (
    SolityApiClient,
    SolityApiClientAuthenticationError,
    SolityApiClientError,
)

if TYPE_CHECKING:
    from datetime import timedelta
    from logging import Logger

    from homeassistant.core import HomeAssistant

    from .data import SolityConfigEntry


class SolityDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the Solity API."""

    config_entry: SolityConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        logger: Logger,
        name: str,
        update_interval: timedelta,
        client: SolityApiClient,
        devices: list[dict[str, Any]],
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass=hass,
            logger=logger,
            name=name,
            update_interval=update_interval,
        )
        self.client = client
        self.devices = devices

    async def _async_update_data(self) -> dict[str, Any]:
        """Update data via library."""
        try:
            # Refresh device list
            self.devices = await self.client.async_get_devices()

            # Build device data dictionary
            data = {}
            for device in self.devices:
                device_id = device.get("myDeviceId", "")
                data[device_id] = {
                    "info": device,
                    "battery": device.get("battery", 0),
                    "is_locked": None,  # Will be updated by lock entity
                    "model": device.get("modelName", "Unknown"),
                    "nickname": device.get("nickname", "Solity Lock"),
                    "firmware": device.get("firmwareVersion", "Unknown"),
                    "gateway_connected": device.get("gatewayConnectionStatus") == "Y",
                }
            return data

        except SolityApiClientAuthenticationError as exception:
            raise ConfigEntryAuthFailed(exception) from exception
        except SolityApiClientError as exception:
            raise UpdateFailed(exception) from exception
