"""
Patient Health Monitoring System - Blynk Service Module
=======================================================
Handles all communication with the Blynk Cloud REST API.

Uses Blynk Cloud REST API endpoints:
  - GET  /external/api/get?token={token}&pin=V{pin}
  - GET  /external/api/update?token={token}&pin=V{pin}&value={value}
  - GET  /external/api/isHardwareConnected?token={token}

This is an educational project for B.Tech college demonstration.
NOT intended for real medical diagnosis.
"""

import os
import logging

import requests
from dotenv import load_dotenv

import config

logger = logging.getLogger(__name__)


class BlynkService:
    """Service class for interacting with Blynk Cloud REST API."""

    def __init__(self):
        """Initialize BlynkService by loading the auth token from .env."""
        self.token = None
        self.connected = False
        self._load_token()

    def _load_token(self):
        """Load Blynk auth token from .env file."""
        try:
            load_dotenv(config.ENV_FILE)
            self.token = os.getenv("BLYNK_AUTH_TOKEN")

            if not self.token or self.token == "YOUR_TOKEN_HERE":
                self.token = None
                logger.warning("Blynk auth token not configured in .env file.")
            else:
                # Log only the first 4 and last 4 characters of the token
                masked = self.token[:4] + "..." + self.token[-4:]
                logger.info("Blynk token loaded: %s", masked)
        except Exception as e:
            logger.error("Error loading .env file: %s", e)
            self.token = None

    def is_configured(self):
        """Check if the Blynk token is configured."""
        return self.token is not None

    def get_masked_token(self):
        """Return a masked version of the token for display."""
        if not self.token:
            return "NOT CONFIGURED"
        return self.token[:4] + "****" + self.token[-4:]

    def check_connection(self):
        """
        Check connection to Blynk Cloud by verifying the device is online.

        Returns:
            tuple: (success: bool, message: str)
        """
        if not self.is_configured():
            return False, "Blynk token not configured."

        try:
            url = f"{config.BLYNK_API_BASE}/isHardwareConnected"
            params = {"token": self.token}
            response = requests.get(url, params=params, timeout=config.BLYNK_TIMEOUT)

            if response.status_code == 200:
                self.connected = True
                logger.info("Blynk connection successful.")
                return True, "Blynk connection successful."
            elif response.status_code == 401:
                self.connected = False
                logger.error("Blynk connection failed: Invalid token.")
                return False, "Invalid Blynk token."
            else:
                self.connected = False
                msg = f"Blynk returned status code: {response.status_code}"
                logger.error("Blynk connection check failed: %s", msg)
                return False, msg

        except requests.exceptions.ConnectionError:
            self.connected = False
            logger.error("Blynk connection failed: No internet connection.")
            return False, "No internet connection or Blynk server unreachable."
        except requests.exceptions.Timeout:
            self.connected = False
            logger.error("Blynk connection failed: Request timed out.")
            return False, "Connection timed out."
        except requests.exceptions.RequestException as e:
            self.connected = False
            logger.error("Blynk connection failed: %s", e)
            return False, f"Connection error: {e}"

    def update_pin(self, pin, value):
        """
        Update a virtual pin value on Blynk Cloud.

        Uses: GET /external/api/update?token={token}&pin=V{pin}&value={value}

        Args:
            pin (int): Virtual pin number (0-4).
            value: Value to send.

        Returns:
            tuple: (success: bool, message: str)
        """
        if not self.is_configured():
            return False, "Blynk token not configured."

        try:
            url = f"{config.BLYNK_API_BASE}/update"
            params = {
                "token": self.token,
                "pin": f"V{pin}",
                "value": value,
            }
            response = requests.get(url, params=params, timeout=config.BLYNK_TIMEOUT)

            if response.status_code == 200:
                logger.info("Blynk pin V%d updated to %s", pin, value)
                return True, f"V{pin} updated to {value}"
            elif response.status_code == 401:
                logger.error("Blynk update failed: Invalid token.")
                return False, "Invalid Blynk token."
            else:
                msg = f"Blynk update failed (status {response.status_code})"
                logger.error(msg)
                return False, msg

        except requests.exceptions.ConnectionError:
            logger.error("Blynk update failed: No connection.")
            return False, "No internet connection."
        except requests.exceptions.Timeout:
            logger.error("Blynk update failed: Timeout.")
            return False, "Connection timed out."
        except requests.exceptions.RequestException as e:
            logger.error("Blynk update failed: %s", e)
            return False, f"Error: {e}"

    def get_pin(self, pin):
        """
        Read a virtual pin value from Blynk Cloud.

        Uses: GET /external/api/get?token={token}&pin=V{pin}

        Args:
            pin (int): Virtual pin number.

        Returns:
            tuple: (success: bool, value_or_message)
        """
        if not self.is_configured():
            return False, "Blynk token not configured."

        try:
            url = f"{config.BLYNK_API_BASE}/get"
            params = {
                "token": self.token,
                "pin": f"V{pin}",
            }
            response = requests.get(url, params=params, timeout=config.BLYNK_TIMEOUT)

            if response.status_code == 200:
                value = response.json()
                # Blynk returns values as a JSON array, e.g. ["1"]
                if isinstance(value, list) and len(value) > 0:
                    value = value[0]
                logger.info("Blynk pin V%d value: %s", pin, value)
                return True, value
            elif response.status_code == 401:
                return False, "Invalid Blynk token."
            else:
                return False, f"Failed to read pin (status {response.status_code})"

        except requests.exceptions.ConnectionError:
            return False, "No internet connection."
        except requests.exceptions.Timeout:
            return False, "Connection timed out."
        except requests.exceptions.RequestException as e:
            return False, f"Error: {e}"

    def send_patient_data(self, heart_rate, spo2, temperature, status_code):
        """
        Send all patient data to Blynk Cloud.

        Args:
            heart_rate (float): Heart rate value.
            spo2 (float): SpO2 value.
            temperature (float): Temperature value.
            status_code (int): Status code (0=NORMAL, 1=WARNING, 2=CRITICAL, 3=EMERGENCY).

        Returns:
            tuple: (success: bool, message: str)
        """
        if not self.is_configured():
            return False, "Blynk token not configured."

        results = []

        # Send Heart Rate → V0
        ok, msg = self.update_pin(config.VPIN_HEART_RATE, heart_rate)
        results.append(("V0 Heart Rate", ok, msg))

        # Send SpO2 → V1
        ok, msg = self.update_pin(config.VPIN_SPO2, spo2)
        results.append(("V1 SpO2", ok, msg))

        # Send Temperature → V2
        ok, msg = self.update_pin(config.VPIN_TEMPERATURE, temperature)
        results.append(("V2 Temperature", ok, msg))

        # Send Status → V3
        ok, msg = self.update_pin(config.VPIN_STATUS, status_code)
        results.append(("V3 Status", ok, msg))

        all_ok = all(r[1] for r in results)
        if all_ok:
            logger.info("All patient data sent to Blynk successfully.")
            return True, "All data sent to Blynk."
        else:
            failed = [r[0] for r in results if not r[1]]
            msg = f"Failed to send: {', '.join(failed)}"
            logger.error(msg)
            return False, msg

    def get_emergency_switch(self):
        """
        Read the emergency switch (V4) from Blynk.

        Returns:
            tuple: (success: bool, switch_state: int or message: str)
                   switch_state: 0 = OFF, 1 = ON
        """
        ok, value = self.get_pin(config.VPIN_EMERGENCY)

        if ok:
            try:
                state = int(value)
                return True, state
            except (ValueError, TypeError):
                return True, 0  # Default to OFF if value is unexpected
        else:
            return False, value
