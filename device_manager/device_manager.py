import sys
sys.path.append('../')
import computer_board.computer_board as ComputerBoard
#import mock_computer_board.mock_computer_board as ComputerBoard
from peristaltic.peristaltic_pump import PeristalticPump
from water_pump.water_pump import WaterPump

#Initialize board pins.
ComputerBoard.Init()

#Peristaltic pumps:
peristaltic_pins = {
    'P1': (18, 25),
    'P2': (27, 12),
    'P3': (16, 20)
}

peristaltic_pumps = {}

#Water pump:
water_pump_pin = 22

water_pump = lambda: None #Empty object (TODO: find cleaner way to do this)

#Initialize device manager:
def Init():
  #Initialize peristaltic pumps:
  for pump_name in peristaltic_pins:
    pump = PeristalticPump(pump_name) 
    peristaltic_pumps[pump_name] = pump
    pin1, pin2 = _PeristalticPinsFromName(pump_name)
    ComputerBoard.InitializePinAsOutput(pin1)
    ComputerBoard.InitializePinAsOutput(pin2)
    pump.Stop()
  #Initialize water pump:
  water_pump = WaterPump() #First declared globally in this module.
  ComputerBoard.InitializePinAsOutput(water_pump_pin)
  water_pump.Stop()


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

def CleanFinalize():
  ComputerBoard.CleanFinalize()
