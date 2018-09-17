import computer_board as ComputerBoard
#import mock_computer_board as ComputerBoard
from peristaltic_pump import PeristalticPump

pump_pins = {
    'P1': (18, 25),
    'P2': (27, 12),
    'P3': (16, 20)
}

pumps = {}

def Init():
  ComputerBoard.Init()
  for pump_name in pump_pins:
    pump = PeristalticPump(pump_name) 
    pumps[pump_name] = pump
    pin1, pin2 = _PumpPinsFromName(pump_name)
    ComputerBoard.InitializePinAsOutput(pin1)
    ComputerBoard.InitializePinAsOutput(pin2)
    StopPump(pump)


def StartPump(peristaltic_pump, dir_forward=True): 
  pin1, pin2 = _PumpPinsFromName(peristaltic_pump.name)
  ComputerBoard.SetOutputToPin(pin1, not dir_forward)
  ComputerBoard.SetOutputToPin(pin2, dir_forward)


def StopPump(peristaltic_pump): 
  pin1, pin2 = _PumpPinsFromName(peristaltic_pump.name)
  ComputerBoard.SetOutputToPin(pin1, False)
  ComputerBoard.SetOutputToPin(pin2, False)


def StopAllPumps():
  for pump in pumps.values():
    StopPump(pump)


def _PumpPinsFromName(pump_name):
    pin1 = pump_pins[pump_name][0]
    pin2 = pump_pins[pump_name][1]
    return pin1, pin2
