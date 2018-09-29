"""Defines the LoadCell class."""
import device_manager as DeviceManager


class LoadCells(object):
    """Models a group of four load cells connected in parallel to a unique amplifier+ADC, allowing us to get the weight of the water reservoir."""

    def __init__(self):
        self._weight = 0

    def get_weight_measurement(self):
        """Returns the weight measurement:

        Returns:
            weight (float): The value of weight measured.
        """

        weight = DeviceManager.get_weight_measurement()
        self._weight = weight
        return self._weight

