"""Defines the LoadCellsReader class."""
import threading
import device_manager as DeviceManager
from time import sleep

class WaterThermometerReader(object):
    """Handles interaction with the DS18B20 water temperature sensor/thermometer."""

    def __init__(self):
        self._temperature = 0

    def configure_thread(self, ds18b20_object):
        self._water_thermometer_thread = threading.Thread(target=self._run_ds18b20_reader, args=(ds18b20_object,))
        self._water_thermometer_thread.setDaemon(True)

    def start(self):
        """Starts the background thread to get measurements from the load cells."""
        self._water_thermometer_thread.start()

    def temp_measurement(self):
        """Returns the water temperature measured."""
        return self._temperature

    def _run_ds18b20_reader(self, ds18b20_object):
        """Method that will be executed in every thread loop."""
        while True:
	        self._temperature = ds18b20_object.read_temp()
	        sleep(1)