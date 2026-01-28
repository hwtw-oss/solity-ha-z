"""Lock platform for Solity LAVO Smart Lock."""

from __future__ import annotations

from typing import Any

from homeassistant.components.lock import LockEntity, LockEntityFeature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, LOGGER
from .coordinator import SolityDataUpdateCoordinator
from .data import SolityConfigEntry


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SolityConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Solity lock entities."""
    coordinator = entry.runtime_data.coordinator
    client = entry.runtime_data.client
    devices = entry.runtime_data.devices

    entities = []
    for device in devices:
        entities.append(
            SolityLock(
                coordinator=coordinator,
                device=device,
                client=client,
            )
        )

    async_add_entities(entities)


class SolityLock(CoordinatorEntity[SolityDataUpdateCoordinator], LockEntity):
    """Representation of a Solity LAVO Smart Lock."""

    _attr_has_entity_name = True
    _attr_supported_features = LockEntityFeature.OPEN

    def __init__(
        self,
        coordinator: SolityDataUpdateCoordinator,
        device: dict[str, Any],
        client: Any,
    ) -> None:
        """Initialize the lock."""
        super().__init__(coordinator)
        self._client = client
        self._device = device
        self._device_id = device.get("myDeviceId", "")
        self._is_locked: bool | None = None

        # Entity attributes
        self._attr_unique_id = f"{DOMAIN}_{self._device_id}_lock"
        self._attr_name = device.get("nickname", "Lock")

        # Device info
        self._attr_device_info = {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": device.get("nickname", "Solity Lock"),
            "manufacturer": device.get("manufacturer", "Solity"),
            "model": device.get("modelName", "LAVO"),
            "sw_version": device.get("firmwareVersion", "Unknown"),
        }

    @property
    def is_locked(self) -> bool | None:
        """Return true if the lock is locked."""
        return self._is_locked

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        if self.coordinator.data is None:
            return False
        device_data = self.coordinator.data.get(self._device_id, {})
        return device_data.get("gateway_connected", False)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        if self.coordinator.data is None:
            return {}

        device_data = self.coordinator.data.get(self._device_id, {})
        return {
            "battery_level": device_data.get("battery", 0),
            "model": device_data.get("model", "Unknown"),
            "firmware": device_data.get("firmware", "Unknown"),
            "gateway_connected": device_data.get("gateway_connected", False),
        }

    async def async_lock(self, **kwargs: Any) -> None:
        """Lock the device."""
        LOGGER.debug("Locking device %s", self._device_id)
        try:
            await self._client.async_lock(self._device_id)
            self._is_locked = True
            self.async_write_ha_state()
        except Exception as err:
            LOGGER.error("Failed to lock device %s: %s", self._device_id, err)
            raise

    async def async_unlock(self, **kwargs: Any) -> None:
        """Unlock the device."""
        LOGGER.debug("Unlocking device %s", self._device_id)
        try:
            await self._client.async_unlock(self._device_id)
            self._is_locked = False
            self.async_write_ha_state()
        except Exception as err:
            LOGGER.error("Failed to unlock device %s: %s", self._device_id, err)
            raise

    async def async_open(self, **kwargs: Any) -> None:
        """Open the lock (same as unlock for this device)."""
        await self.async_unlock(**kwargs)
