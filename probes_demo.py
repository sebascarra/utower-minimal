#!/usr/bin/env python

import sys
from time import sleep
import device_manager as DeviceManager

def main():

  DeviceManager.Init() #This is mandatory to use any of the available peristaltic pumps. Pump objects are created during the initialization of the DeviceManager.

  probes = DeviceManager.probes

  print('Displaying probe measurements...')  
  while True:
    try:
      print "measurements: ", probes.getMeasurements() #From this point on we use exclusively functions inside the pump class, NOT the DeviceManager module.
      sleep(4)
    except(KeyboardInterrupt):
      # If a keyboard interrupt is detected then it exits cleanly!
      print('Finishing up!')
      quit()

if __name__ == "__main__":
  main()
