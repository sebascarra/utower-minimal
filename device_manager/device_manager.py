from __future__ import absolute_import
#import computer_board.computer_board as ComputerBoard
import mock_computer_board.mock_computer_board as ComputerBoard

pump_pins = {
    'P1': (18, 25),
    'P2': (27, 12),
    'P3': (16, 20)
}

pumps = {}

def Init():
  import peristaltic.peristaltic_pump as Peristaltic
  ComputerBoard.Init()
  for pump_name in pump_pins:
    pump = Peristaltic.PeristalticPump(pump_name) 
    pumps[pump_name] = pump
    pin1, pin2 = _PumpPinsFromName(pump_name)
    ComputerBoard.InitializePinAsOutput(pin1)
    ComputerBoard.InitializePinAsOutput(pin2)
    pump.Stop()


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
    pump.Stop()

def _PumpPinsFromName(pump_name):
    pin1 = pump_pins[pump_name][0]
    pin2 = pump_pins[pump_name][1]
    return pin1, pin2

def CleanFinalize():
  ComputerBoard.CleanFinalize()
