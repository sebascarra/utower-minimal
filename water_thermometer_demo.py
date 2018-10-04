#!/usr/bin/env python
"""Contains a sample that tests the DS18B20 water temperature sensor/thermometer."""
from __future__ import print_function
from time import sleep
import device_manager as DeviceManager


def main():
    """Prints the temperature measured by the water thermometer to stdout."""
   
    # First initialize the device manager. This is mandatory to use the water thermometer.
    # A water thermometer object is created during the initialization of the DeviceManager.
    DeviceManager.init("water_thermometer")

    water_thermometer = DeviceManager.water_thermometer

    # From this point on we use exclusively functions inside the WaterThermometer class,
    # NOT the DeviceManager module.

    print('Displaying water temperature measurements...')

    try:
        while True:
            print("Temperature: ", str(water_thermometer.get_temperature_measurement()))
            sleep(3)
    except KeyboardInterrupt:
        # If a keyboard interrupt is detected then it exits cleanly!
        print('Finishing up!')
    finally:
        # Freeing up resources is done through the device manager as it is the one that knows
        # if the water thermometer exists.
        DeviceManager.clean_finalize() # This ensures a clean exit
        #quit()


if __name__ == "__main__":
    main()
