#!/usr/bin/env python

import sys
from time import sleep
import device_manager as DeviceManager

def main():

  DeviceManager.Init() # This is mandatory to use any of the available probes. Probe objects are created during the initialization of the DeviceManager.

  probes = DeviceManager.probes

  print('Displaying probe measurements...')  
  while True:
    try:
      print "measurements: ", probes.getMeasurements() #From this point on we use exclusively functions inside the probe class, NOT the DeviceManager module.
      sleep(4)
    except(KeyboardInterrupt):
      # If a keyboard interrupt is detected then it exits cleanly!
      print('Finishing up!')
    finally: #Freeing up resources is done through the device manager as it is the one that knows what probes exist.
      DeviceManager.CleanFinalize() #This ensures a clean exit
      quit()

if __name__ == "__main__":
  main()
