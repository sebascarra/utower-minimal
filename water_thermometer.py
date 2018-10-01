"""Defines the LoadCell class."""
import device_manager as DeviceManager


class WaterThermometer(object):
    """Models a group of four load cells connected in parallel to a unique amplifier+ADC, allowing us to get the weight of the water reservoir."""

    def __init__(self):
        self._temperature = 0

    def get_temperature_measurement(self):
        """Returns the temperature measurement:

        Returns:
            temperature (float): The value of temperature measured.
        """

        self._temperature = DeviceManager.get_temperature_measurement()
        return self._temperature

