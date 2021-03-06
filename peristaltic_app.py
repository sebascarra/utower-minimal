#!/usr/bin/env python
"""Contains a sample that tests the peristaltic pumps."""
from __future__ import print_function
import sys
from time import sleep
import device_manager as DeviceManager

# Correct usage:
# -ComputerBoard knows what platform is being used and its physical characteristics.
# -DeviceManager knows the type and quantity of actuators used, and to what "pins" they
#      are connected on the specific platform in use (but it does NOT know what the platform
#      is, it only knows that it has "pins")
# -DeviceManager may use a real physical ComputerBoard or a "mock" simulated one.
# -Since DeviceManager knows the type, quantity and name of actuators/sensors, there is no
#      option other than to initialize all actuators and sensors through DeviceManager methods.
# -Other than initializing sensors/actuators and freeing up resources, the attributes and methods
#      related to sensors/actuators to be used have to be in the specific module of that
#      sensor/actuator.

# Example:

def main(argv):
    """Makes each peristaltic pump turn to both sides and stop."""

    # First initialize the device manager. This is mandatory to use any of the available
    # peristaltic pumps. Pump objects are created during the initialization of the DeviceManager.
    DeviceManager.init("peristaltic_pump")

    # The name of the pump to be tested is received as an argument.
    mode = argv[1]
    pump_name = argv[2]

    try:
        # Get pump object for the pump to be tested.
        pump = DeviceManager.peristaltic_pumps[pump_name]
    except KeyError:
        print('Pump [{}] does not exist.'.format(pump_name))
        raise

    if mode == "start":
        if int(argv[3]) == 0:
            pump_direction = False
        else:
            pump_direction = True
        pump.start(pump_direction)
    elif mode == "stop":
        pump.stop()
        DeviceManager.clean_finalize() # This ensures a clean exit

if __name__ == "__main__":
    main(sys.argv)
