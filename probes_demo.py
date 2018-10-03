#!/usr/bin/env python
"""Contains a sample that tests the EC and PH probes."""
from __future__ import print_function
from time import sleep
import device_manager as DeviceManager


def main():
    """Prints the measurements from the EC and PH probes to stdout."""

    # First initialize the device manager. This is mandatory to use any of the available
    # probes. Probe objects are created during the initialization of the DeviceManager.
    DeviceManager.init()

    probes = DeviceManager.probes

    # From this point on we use exclusively functions inside the probe class,
    # NOT the DeviceManager module.

    print('Displaying probe measurements...')

    try:
        while True:
            print("measurements: ", probes.get_measurements())
            sleep(1)
    except KeyboardInterrupt:
        # If a keyboard interrupt is detected then it exits cleanly!
        print('Finishing up!')
    finally:
        # Freeing up resources is done through the device manager as it is the one that knows
        # what pumps exist.
        DeviceManager.clean_finalize() # This ensures a clean exit
        #quit()


if __name__ == "__main__":
    main()
