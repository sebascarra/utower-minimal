#!/usr/bin/env python

# A program to control the movement of a single motor using the RTK MCB!
# Composed by The Raspberry Pi Guy to accompany his tutorial!

# Let's import the modules we will need!
from time import sleep
import RPi.GPIO as GPIO
import sys

class ComputerBoard(object):
# TODO: move to modules
  @staticmethod
  def Init():
    GPIO.setmode(GPIO.BCM)

  @staticmethod
  def SetOutputToPin(pin_number, state) 
    GPIO.output(pin_number, state)

  @staticmethod
  def InitializePinAsOutput(pin_number):
    GPIO.setup(pin_number, GPIO.OUT)


class DeviceManager(object):
  
  pump_pins = {
      'P1': (18, 25),
      'WP': (22, 22),
      'P2': (27, 12),
      'P3': (16, 20)
  }

  pumps = {}

  @staticmethod
  def Init():
    for pump_name in pump_pins:
      pump = PeristalticPump(pump_name) 
      pumps[pump_name] = pump
      pin1 = pump_pins[pump_name][0]
      pin2 = pump_pins[pump_name][1]
      ComputerBoard.InitializePinAsOutput(pin1)
      ComputerBoard.InitializePinAsOutput(pin2)
      StopPump(pump)

  
  @staticmethod
  def StartPump(persitaltic_pump, dir_forward=True): 
    
    pin1 = pump_pinss[peristaltic_pump.name][0]
    pin2 = pump_pins[peristaltic_pump.name][1]

    ComputerBoard.SetOutputToPin(pin1, not dir_forward)
    ComputerBoard.SetOutputToPin(pin2, dir_forward)

  @staticmethod
  def StopPump(persitaltic_pump): 
    
    pin1 = pumps[peristaltic_pump.name][0]
    pin2 = pumps[peristaltic_pump.name][1]

    ComputerBoard.SetOutputToPin(pin1, False)
    ComputerBoard.SetOutputToPin(pin2, False)

  @staticmethod
  def StopAllPumps()
    for pump in pumps.values():
      StopPump(pump)


class PeristalticPump(object):

  def _init_(self, name):
    self._name = name
    self._is_on = False
    
  def Start(dir_forward=True):
    DeviceManager.StartPump(self, dir_forward)
    self._is_on = True

  def Stop():
    DeviceManager.StopPump(self)
    self._is_on = False

def main(argv):

  DeviceManager.Init() 
  
  pump_name = sys.argv[1]
  try:
    pump = DeviceManager.pumps[pump_name]
  except KeyError as e:
    print('Pump [{}] does not exist.'.format(pump_name))

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
