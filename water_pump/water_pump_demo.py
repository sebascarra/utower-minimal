#!/usr/bin/env python

from time import sleep
import device_manager as DeviceManager

def main():

  DeviceManager.Init() 

  pump = DeviceManager.pump

  print('Starting motor sequence!')

  while True:
    try:
      DeviceManager.StartPump()
      sleep(3)
      DeviceManager.StopPump()
      sleep(1)
    except(KeyboardInterrupt):
      # If a keyboard interrupt is detected then it exits cleanly!
      DeviceManager.StopPump()
      print('Finishing up!')
      quit()


if __name__ == "__main__":
  main()
