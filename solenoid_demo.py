#!/usr/bin/env python
"""Contains a sample that tests solenoid valve."""
from __future__ import print_function
from time import sleep
import device_manager as DeviceManager


def main():
    # First initialize the device manager.
    DeviceManager.init("solenoid_valve")

    valve = DeviceManager.solenoid_valve

    # From this point on we use exclusively functions inside the SolenoidValve class,
    # NOT the DeviceManager module.

    try:
        while True:
            valve.open()
            sleep(2)
            valve.close()
            sleep(2)
    except KeyboardInterrupt:
            # If a keyboard interrupt is detected then it exits cleanly!
            valve.stop()
            print('Finishing up!')
    finally:
            # Freeing up resources is done through the device manager as it is the one that knows
            # what pumps exist.
            DeviceManager.clean_finalize() # This ensures a clean exit
            quit()


if __name__ == "__main__":
    main()
