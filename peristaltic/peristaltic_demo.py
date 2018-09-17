#!/usr/bin/env python

# A program to control the movement of a single motor using the RTK MCB!
# Composed by The Raspberry Pi Guy to accompany his tutorial!

# Let's import the modules we will need!
from time import sleep
import sys
import device_manager as DeviceManager

def main(argv):

  DeviceManager.Init() 
  
  pump_name = sys.argv[1]
  try:
    pump = DeviceManager.pumps[pump_name]
  except KeyError as e:
    print('Pump [{}] does not exist.'.format(pump_name))
    raise

  print('Starting motor sequence!')  
  while True:
    try:
      DeviceManager.StartPump(pump, dir_forward=True)
      sleep(3)
      DeviceManager.StopPump(pump)
      sleep(1)
      DeviceManager.StartPump(pump, dir_forward=False)
      sleep(3)
      DeviceManager.StopPump(pump)
      sleep(1)
    except(KeyboardInterrupt):
      # If a keyboard interrupt is detected then it exits cleanly!
      DeviceManager.StopAllPumps()
      print('Finishing up!')
      quit()


if __name__ == "__main__":
  main(sys.argv)
