import computer_board as ComputerBoard
#import mock_computer_board as ComputerBoard
from water_pump import WaterPump

pump_pin = 22

pump = {}

def Init():
  pump = WaterPump()
  ComputerBoard.Init()
  ComputerBoard.InitializePinAsOutput(pump_pin)
  StopPump()

def StartPump():
  ComputerBoard.SetOutputToPin(pump_pin, True)

def StopPump():
  ComputerBoard.SetOutputToPin(pump_pin, False)
