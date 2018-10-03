#!/usr/bin/env python
from __future__ import print_function
import sys
from time import sleep
import device_manager as DeviceManager

def main():
    DeviceManager.init("stepper_motor")
    stepper = DeviceManager.stepper
    stepper.stop()
    DeviceManager.clean_finalize()

if __name__ == "__main__":
    main()
