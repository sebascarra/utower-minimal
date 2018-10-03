#!/usr/bin/env python
"""Contains a sample application using all the elements that make up UTower. All classes are used."""
from __future__ import print_function
import sys
from time import sleep
import device_manager as DeviceManager


def main(argv):
    """Makes each peristaltic pump turn to both sides and stop."""

    # First initialize the device manager. This is mandatory to use any of the available
    # peristaltic pumps. Pump objects are created during the initialization of the DeviceManager.
    DeviceManager.init()

    #Initialize peristaltic pumps:
    #TODO

    #Initialize water pump:
    water_pump = DeviceManager.water_pump

    #Initialize EC and pH probes:
    probes = DeviceManager.probes

    #Initialize solenoid valve:
    valve = DeviceManager.solenoid_valve

    #Initialize load cells:
    cells = DeviceManager.load_cells_object

    #Init

    # From this point on we use exclusively functions inside the pump class,
    # NOT the DeviceManager module.

    print('Starting demo application!')

    try:
        while True:
            pump.start()
            sleep(3)
            pump.stop()
            sleep(1)
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
        #quit()

if __name__ == "__main__":
    main(sys.argv)
