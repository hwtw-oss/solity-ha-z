"""Constants for Solity LAVO integration."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "solity"
ATTRIBUTION = "Data provided by Solity Smart Lock API"

# API Constants
API_BASE_URL = "https://www.smartsolity.com/api_v2"

# BLE UUIDs (for future BLE support)
BLE_WRITE_UUID = "48400002-B5A3-F393-E0A9-E50E24DCCA9E"
BLE_NOTIFY_UUID = "48400003-B5A3-F393-E0A9-E50E24DCCA9E"

# Device control commands
CMD_CONNECT_GATEWAY = "connect_gateway"
CMD_GET_STATUS = "get_status"
CMD_OPEN = "open"
CMD_CLOSE = "close"
CMD_GET_FINGERPRINT = "get_fingerprint"
CMD_GET_PASSWORD_INFO = "get_pwdinfo"
