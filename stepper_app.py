#!/usr/bin/env python
"""Contains a sample that tests the stepper motor."""
from __future__ import print_function
import sys
from time import sleep
import device_manager as DeviceManager


def main(argv):
    """Makes each peristaltic pump turn to both sides and stop."""

    # First initialize the device manager. This is mandatory to use the stepper motor.
    # A stepper motor object is created during the initialization of the DeviceManager.
    DeviceManager.init("stepper_motor")

    stepper = DeviceManager.stepper

    mode = argv[1]

    # From this point on we use exclusively functions inside the StepperMotor class,
    # NOT the DeviceManager module.

    if (mode == "start"):
        stepper.start(dir_forward=True)
    elif (mode == "stop"):
        stepper.stop()
        DeviceManager.clean_finalize() # This ensures a clean exit

if __name__ == "__main__":
    main(sys.argv)
