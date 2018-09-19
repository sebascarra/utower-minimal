#!/usr/bin/env python

import sys
from time import sleep
import device_manager as DeviceManager

def main():

  DeviceManager.Init() 

  pump = DeviceManager.water_pump

  print('Starting motor sequence!')

  while True:
    try:
      pump.Start()
      sleep(3)
      pump.Stop()
      sleep(1)
    except(KeyboardInterrupt):
      # If a keyboard interrupt is detected then it exits cleanly!
      pump.Stop()
      print('Finishing up!')
      quit()
      


if __name__ == "__main__":
  main()
