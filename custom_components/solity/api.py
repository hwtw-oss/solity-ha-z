"""Solity LAVO API Client."""

from __future__ import annotations

import socket
from typing import Any

import aiohttp
import async_timeout

from .const import API_BASE_URL, CMD_CLOSE, CMD_GET_STATUS, CMD_OPEN


class SolityApiClientError(Exception):
    """Exception to indicate a general API error."""


class SolityApiClientCommunicationError(SolityApiClientError):
    """Exception to indicate a communication error."""


class SolityApiClientAuthenticationError(SolityApiClientError):
    """Exception to indicate an authentication error."""


def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """Verify that the response is valid."""
    if response.status in (401, 403):
        msg = "Invalid credentials"
        raise SolityApiClientAuthenticationError(msg)
    response.raise_for_status()


class SolityApiClient:
    """Solity LAVO API Client."""

    def __init__(
        self,
        username: str,
        password: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Initialize the API client."""
        self._username = username
        self._password = password
        self._session = session
        self._auth_token: str | None = None
        self._auth_pwd: str | None = None

    async def async_login(self) -> dict[str, Any]:
        """Login to Solity API and get auth tokens."""
        data = {
            "email": self._username,
            "password": self._password,
        }
        response = await self._api_wrapper(
            method="post",
            url=f"{API_BASE_URL}/login",
            data=data,
        )

        if response.get("result") != 0:
            raise SolityApiClientAuthenticationError(
                response.get("errorMessage", "Login failed")
            )

        # Store auth tokens from response
        contents = response.get("contents", {})
        self._auth_token = contents.get("authToken", "")
        self._auth_pwd = contents.get("authPwd", "")

        return response

    async def async_get_devices(self) -> list[dict[str, Any]]:
        """Get list of devices from the API."""
        if not self._auth_token:
            await self.async_login()

        response = await self._api_wrapper(
            method="get",
            url=f"{API_BASE_URL}/myDevice",
            headers=self._get_auth_headers(),
        )

        if response.get("result") != 0:
            raise SolityApiClientError(
                response.get("errorMessage", "Failed to get devices")
            )

        contents = response.get("contents", {})
        return contents.get("myDeviceList", [])

    async def async_get_device_status(self, device_id: str) -> dict[str, Any]:
        """Get status of a specific device."""
        if not self._auth_token:
            await self.async_login()

        response = await self._api_wrapper(
            method="put",
            url=f"{API_BASE_URL}/controlDevice/{device_id}",
            data={"command": CMD_GET_STATUS},
            headers=self._get_auth_headers(),
        )

        return response

    async def async_lock(self, device_id: str) -> dict[str, Any]:
        """Lock the device."""
        if not self._auth_token:
            await self.async_login()

        response = await self._api_wrapper(
            method="put",
            url=f"{API_BASE_URL}/controlDevice/{device_id}",
            data={"command": CMD_CLOSE},
            headers=self._get_auth_headers(),
        )

        return response

    async def async_unlock(self, device_id: str) -> dict[str, Any]:
        """Unlock the device."""
        if not self._auth_token:
            await self.async_login()

        response = await self._api_wrapper(
            method="put",
            url=f"{API_BASE_URL}/controlDevice/{device_id}",
            data={"command": CMD_OPEN},
            headers=self._get_auth_headers(),
        )

        return response

    async def async_get_logs(
        self, device_id: str, page: int = 1
    ) -> list[dict[str, Any]]:
        """Get device activity logs."""
        if not self._auth_token:
            await self.async_login()

        response = await self._api_wrapper(
            method="get",
            url=f"{API_BASE_URL}/retrieveLog/page/{device_id}?page={page}",
            headers=self._get_auth_headers(),
        )

        contents = response.get("contents", {})
        return contents.get("logList", [])

    def _get_auth_headers(self) -> dict[str, str]:
        """Get authentication headers."""
        return {
            "Authorization": self._auth_token or "",
            "AuthorizationPwd": self._auth_pwd or "",
            "User-Agent": "okhttp/4.9.1",
            "Content-Type": "application/json",
            "Accept-Encoding": "gzip",
        }

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> Any:
        """Make API request with error handling."""
        if headers is None:
            headers = {
                "User-Agent": "okhttp/4.9.1",
                "Content-Type": "application/json",
            }

        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                )
                _verify_response_or_raise(response)
                return await response.json()

        except TimeoutError as exception:
            msg = f"Timeout error fetching information - {exception}"
            raise SolityApiClientCommunicationError(msg) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise SolityApiClientCommunicationError(msg) from exception
        except Exception as exception:
            msg = f"Unexpected error - {exception}"
            raise SolityApiClientError(msg) from exception
