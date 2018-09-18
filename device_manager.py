import sys
import computer_board as ComputerBoard
#import mock_computer_board as ComputerBoard
from peristaltic_pump import PeristalticPump
from water_pump import WaterPump

#Initialize board pins to be used by hardware components.
ComputerBoard.Init()

#Set up hardware components: #################################################

  #Peristaltic pumps:
peristaltic_pins = {
    'P1': (18, 25),
    'P2': (27, 12),
    'P3': (16, 20)
}

peristaltic_pumps = {}

  #Water pump:
water_pump_pin = 22

water_pump = None #For cleaniness, this is set to an initial value during Init(). 

#End of setup of hardware components #########################################

#Initialize device manager:
def Init():
  #Initialize peristaltic pumps:
  for pump_name in peristaltic_pins:
    pump = PeristalticPump(pump_name) 
    peristaltic_pumps[pump_name] = pump # -> Why we don't need to use the "global" keyword here: https://stackoverflow.com/questions/14323817/global-dictionaries-dont-need-keyword-global-to-modify-them
    pin1, pin2 = _PeristalticPinsFromName(pump_name)
    ComputerBoard.InitializePinAsOutput(pin1)
    ComputerBoard.InitializePinAsOutput(pin2)
    pump.Stop()
  #Initialize water pump:
  global water_pump #See (*) at bottom.
  water_pump = WaterPump() 
  ComputerBoard.InitializePinAsOutput(water_pump_pin)
  water_pump.Stop()

#Auxiliary functions: ########################################################

def StartPump(pump, dir_forward=True):
  if pump.name != 'WP':
    #Procedure for peristaltics:
    pin1, pin2 = _PeristalticPinsFromName(pump.name)
    ComputerBoard.SetOutputToPin(pin1, not dir_forward)
    ComputerBoard.SetOutputToPin(pin2, dir_forward)
    #Procedure for water pump:
  else:
    ComputerBoard.SetOutputToPin(water_pump_pin, True)

def StopPump(pump):
  if pump.name != 'WP':
    #Procedure for peristaltics:
    pin1, pin2 = _PeristalticPinsFromName(pump.name)
    ComputerBoard.SetOutputToPin(pin1, False)
    ComputerBoard.SetOutputToPin(pin2, False)
  else:
    #Procedure for water pump:
    ComputerBoard.SetOutputToPin(water_pump_pin, False)

def StopAllPumps():
  #Procedure for peristaltics:
  for pump in peristaltic_pumps.values():
    pump.Stop()
  #Procedure for water pump:
  water_pump.Stop()
  

def _PeristalticPinsFromName(pump_name):
    pin1 = peristaltic_pins[pump_name][0]
    pin2 = peristaltic_pins[pump_name][1]
    return pin1, pin2

#End of auxiliary functions. ###################################################

#Clean up after exit.
def CleanFinalize():
  ComputerBoard.CleanFinalize()

#(*):

# From: https://stackoverflow.com/questions/10588317/python-function-global-variables
# 303
# down vote
# accepted
# If you want to simply access a global variable you just use its name. However to change its value you need to use the global keyword.
# E.g.
# global someVar
# someVar = 55
# This would change the value of the global variable to 55. Otherwise it would just assign 55 to a local variable.

# 75
# down vote
# Within a Python scope, any assignment to a variable not already declared within that scope creates a new local variable unless that variable is declared earlier in the function as referring to a globally scoped variable with the keyword global.