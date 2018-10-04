#!/usr/bin/env python
"""Contains a sample that tests the load cells."""
from __future__ import print_function
from time import sleep
import device_manager as DeviceManager


def main():
    """Prints the weight measured by the group of load cells to stdout."""
   
    # First initialize the device manager. This is mandatory to use the group of load cells.
    # A load cell group object is created during the initialization of the DeviceManager.
    DeviceManager.init("load_cells")

    cells = DeviceManager.load_cells_object

    # From this point on we use exclusively functions inside the LoadCells class,
    # NOT the DeviceManager module.top

    try:
        while True:
            #Sleep both here and in the thread loop result in better CPU usage than just putting "pass" in the main while loop.
            sleep(0.2)
            #print(str(cells.get_weight_measurement() / 1))
            #sleep(0.5)
    finally:
        # Freeing up resources is done through the device manager as it is the one that knows
        # if the group of load cells exists.
        DeviceManager.clean_finalize() # This ensures a clean exit
        #quit()


if __name__ == "__main__":
    main()
