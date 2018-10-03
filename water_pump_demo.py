#!/usr/bin/env python
"""Conatins a sample that tests the EC and PH probes."""
from __future__ import print_function
from time import sleep
import device_manager as DeviceManager

def main():
    """Makes the water pump turn on and off.""" 

    # First initialize the device manager. This is mandatory to use any of the available
    # probes. Probe objects are created during the initialization of the DeviceManager.
    DeviceManager.init("water_pump")

    pump = DeviceManager.water_pump

    # From this point on we use exclusively functions inside the probe class,
    # NOT the DeviceManager module.

    print('Starting motor sequence!')

    try:
        while True:
            pump.start()
            sleep(3)
            pump.stop()
            sleep(1)
    except KeyboardInterrupt:
        # If a keyboard interrupt is detected then it exits cleanly!
        pump.stop()
        print('Finishing up!')
    finally:
        # Freeing up resources is done through the device manager as it is the one that knows
        # what pumps exist.
        DeviceManager.clean_finalize() # This ensures a clean exit
        quit()


if __name__ == "__main__":
    main()
