"""Defines the WaterPump class."""
import device_manager as DeviceManager


class WaterPump(object):
    """Models a water pump object, allowint to start and stop it."""

    def __init__(self):
        self._name = 'WP'
        self._is_on = False

    @property
    def name(self):
        """Returns the name of the pump."""
        return self._name

    def start(self):
        """Starts the pump."""
        DeviceManager.start_pump(self)
        self._is_on = True

    def stop(self):
        """Stops the pump."""
        DeviceManager.stop_pump(self)
        self._is_on = False

