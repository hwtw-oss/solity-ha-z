"""Sensor platform for Solity LAVO Smart Lock."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import PERCENTAGE
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import SolityDataUpdateCoordinator

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .data import SolityConfigEntry


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SolityConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Solity sensor entities."""
    coordinator = entry.runtime_data.coordinator
    devices = entry.runtime_data.devices

    entities = []
    for device in devices:
        entities.append(
            SolityBatterySensor(
                coordinator=coordinator,
                device=device,
            )
        )

    async_add_entities(entities)


class SolityBatterySensor(CoordinatorEntity[SolityDataUpdateCoordinator], SensorEntity):
    """Battery sensor for Solity LAVO Smart Lock."""

    _attr_has_entity_name = True
    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = PERCENTAGE

    def __init__(
        self,
        coordinator: SolityDataUpdateCoordinator,
        device: dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self._device_id = device.get("myDeviceId", "")

        # Entity attributes
        self._attr_unique_id = f"{DOMAIN}_{self._device_id}_battery"
        self._attr_name = "Battery"

        # Device info
        self._attr_device_info = {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": device.get("nickname", "Solity Lock"),
            "manufacturer": device.get("manufacturer", "Solity"),
            "model": device.get("modelName", "LAVO"),
            "sw_version": device.get("firmwareVersion", "Unknown"),
        }

    @property
    def native_value(self) -> int | None:
        """Return the battery level."""
        if self.coordinator.data is None:
            return None
        device_data = self.coordinator.data.get(self._device_id, {})
        return device_data.get("battery", 0)

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        if self.coordinator.data is None:
            return False
        device_data = self.coordinator.data.get(self._device_id, {})
        return device_data.get("gateway_connected", False)
