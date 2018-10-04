#!/usr/bin/env python
"""Conatins a sample that tests the EC and PH probes."""
from __future__ import print_function
import sys
from time import sleep
import device_manager as DeviceManager

def main(argv):
    """Makes the water pump turn on and off.""" 

    # First initialize the device manager. This is mandatory to use any of the available
    # probes. Probe objects are created during the initialization of the DeviceManager.
    DeviceManager.init("water_pump")

    pump = DeviceManager.water_pump

    mode = argv[1]

    # From this point on we use exclusively functions inside the probe class,
    # NOT the DeviceManager module.

    if mode == "start":
        pump.start()
    elif mode == "stop":
        pump.stop()
        DeviceManager.clean_finalize() # This ensures a clean exit

if __name__ == "__main__":
    main(sys.argv)
