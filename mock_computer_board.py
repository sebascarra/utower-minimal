import threading
from random import random

def Init():
  print('GPIO.setmode(GPIO.BCM)')

def SetOutputToPin(pin_number, state):
  print(
    'GPIO.output({pin_number}, {state})'
    .format(pin_number=pin_number, state=state)
  )

def InitializePinAsOutput(pin_number):
  print(
    'GPIO.setup({pin_number}, GPIO.OUT)'
    .format(pin_number=pin_number)
  )

def CleanFinalize():
  print(
    'GPIO.cleanup()'
  )



class ProbeSerialReader(object):
  #Original code: https://stackoverflow.com/questions/39176985/how-to-pipe-data-from-dev-ttyusb0-to-a-python-script
  #For custom readline definition See: https://stackoverflow.com/questions/16470903/pyserial-2-6-specify-end-of-line-in-readline

  def __init__(self, ec_port, ph_port):
    self._ec = 0.00
    self._ph = 0.00
    self._ec_port = None
    self._ph_port = None
    self._serialPortsThread = threading.Thread(target=self._serialReader())
    self._serialPortsThread.setDaemon(True)
    
  @property
  def measurements(self):
    return (self._ec, self._ph)

  def _serialReader(self):
    while True:
        ec = random()
        ph = random()
        if ec > 0.8:
            self._ec = ec
        if ph > 0.8:
            self._ph = ph

  def Init():
      _serialPortsThread.start()
      #_serialPortsThread.join()

# (*): The function node takes only one parameter, but is located in a class. Given the implicit class instance and your parameter, that's 2 arguments. To fix it, you can edit the function to
#      def _readline(self, serialPort):
# See for further details: https://stackoverflow.com/questions/31620212/why-does-this-error-say-im-giving-the-function-two-arguments
