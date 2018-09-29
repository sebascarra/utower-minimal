"""Defines the PeristalticPump class."""
import device_manager as DeviceManager


class PeristalticPump(object):
    """Models a peristaltic pump object, allowing to start and top it."""

    def __init__(self, name):
        self._name = name
        self._is_on = False

    @property
    def name(self):
        """Returns the name of the pump."""
        return self._name

    def start(self, dir_forward=True):
        """Starts the pump in the specified direction.

        Args:
            dir_forward (bool, optional): Whether the pump should be moved in
                the forward direction. Defaults to True.
        """
        DeviceManager.start_pump(self, dir_forward)
        self._is_on = True

    def stop(self):
        """Stops the pump."""
        DeviceManager.stop_pump(self)
        self._is_on = False


