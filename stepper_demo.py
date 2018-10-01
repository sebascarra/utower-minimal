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
    DeviceManager.init()

    stepper = DeviceManager.stepper

    # From this point on we use exclusively functions inside the StepperMotor class,
    # NOT the DeviceManager module.

    print('Starting stepper motor')

    try:
        stepper.start(dir_forward=False)
        while True:
            pass
    except KeyboardInterrupt:
        # If a keyboard interrupt is detected then it exits cleanly!
        stepper.stop()
        print('Finishing up!')
    finally:
        # Freeing up resources is done through the device manager as it is the one that knows
        # what pumps exist.
        DeviceManager.clean_finalize() # This ensures a clean exit
        #quit()

if __name__ == "__main__":
    main(sys.argv)
