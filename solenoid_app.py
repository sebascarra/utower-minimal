#!/usr/bin/env python
"""Contains a sample that tests solenoid valve."""
from __future__ import print_function
import sys
from time import sleep
import device_manager as DeviceManager


def main(argv):
    # First initialize the device manager.
    DeviceManager.init("solenoid_valve")

    valve = DeviceManager.solenoid_valve

    # From this point on we use exclusively functions inside the SolenoidValve class,
    # NOT the DeviceManager module.

    mode = argv[1]

    print (mode)
    if mode == "open":
        valve.open()
    elif mode == "close":
        valve.close()
        DeviceManager.clean_finalize() # This ensures a clean exit

if __name__ == "__main__":
    main(sys.argv)
