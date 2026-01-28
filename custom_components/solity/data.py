"""Custom types for Solity integration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import SolityApiClient
    from .coordinator import SolityDataUpdateCoordinator


type SolityConfigEntry = ConfigEntry[SolityData]


@dataclass
class SolityData:
    """Data for the Solity integration."""

    client: SolityApiClient
    coordinator: SolityDataUpdateCoordinator
    integration: Integration
    devices: list[dict[str, Any]]
