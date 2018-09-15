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
  
  pumps = {'P1': (18, 25), #Dictionary
           'WP': (22, 22),
           'P2': (27, 12),
           'P3': (16, 20)
  }

  # TODO: create static array of pumps.
  
  @staticmethod
  def Init():
    # TODO: add other pumps from dictionary
    # TODO: add new pump to the static array.
    pump1 = PeristalticPump('P1') 
    pin1 = pumps[pump1.name][0]
    pin2 = pumps[pump1.name][1]
    ComputerBoard.InitializePinAsOutput(pin1)
    ComputerBoard.InitializePinAsOutput(pin2)
    StopPump(pump1)

  
  @staticmethod
  def StartPump(persitaltic_pump): 
    
    pin1 = pumps[peristaltic_pump.name][0]
    pin2 = pumps[peristaltic_pump.name][1]

    ComputerBoard.SetOutputToPin(pin1, False)
    ComputerBoard.SetOutputToPin(pin2, True)

  @staticmethod
  def StopPump(persitaltic_pump): 
    
    pin1 = pumps[peristaltic_pump.name][0]
    pin2 = pumps[peristaltic_pump.name][1]

    ComputerBoard.SetOutputToPin(pin1, False)
    ComputerBoard.SetOutputToPin(pin2, False)


class PeristalticPump(object):

  def _init_(self, name):
    self._name = name
    self._is_on = False
    
  def Start():
    #TODO: add direction
    DeviceManager.StartPump(self)
    self._is_on = True

  def Stop():
    DeviceManager.StopPump(self)
    self._is_on = False

def main():

  pumpName = sys.argv[1]

  try:
    DeviceManager.Init() 
    print('Starting motor sequence!')
  
    while True:
      try:
        # TODO: ask device manager to start and stop pumps
        
        #Start pump
        sleep(3)
        # Stop pump
        sleep(1)
      except(KeyboardInterrupt):
        # TODO: ask device manager to stop pumps
        # If a keyboard interrupt is detected then it exits cleanly!
        print('Finishing up!')
        quit()
  except:
    print('Pump does not exist.')


