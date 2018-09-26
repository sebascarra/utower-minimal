"""Defines the SolenoidValve class."""
import device_manager as DeviceManager


class SolenoidValve(object):
    """Models a solenoid valve object, allowing it to open and close."""

    def __init__(self):
        self._is_open = False

    def open(self, dir_forward=True):
        """Opens the solenoid valve."""
        DeviceManager.open_valve()
        self._is_open = True

    def close(self):
        """Shuts/closes the solenoid valve."""
        DeviceManager.close_valve()
        self._is_open = False


