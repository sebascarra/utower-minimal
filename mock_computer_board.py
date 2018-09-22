from __future__ import print_function
import threading
import sys


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


class MockSerial(object):
  
  def __init__(self, port, rate):
    print("MockSerial.__init__()", file=sys.stderr)
    self._port = port
    self._rate = rate

  def read(self, n):
#    print("MockSerial.read()", file=sys.stderr)
    return "text line\r"


class ProbeSerialReader(object):
  #Original code: https://stackoverflow.com/questions/39176985/how-to-pipe-data-from-dev-ttyusb0-to-a-python-script
  #For custom readline definition See: https://stackoverflow.com/questions/16470903/pyserial-2-6-specify-end-of-line-in-readline

  def __init__(self, ec_port, ph_port):
    print("ProbeSerialReader.__init__()", file=sys.stderr)
    self._ec = 0.00
    self._ph = 0.00
    self._ec_port = MockSerial(ec_port, 9600)
    self._ph_port = MockSerial(ph_port, 9600)
    self._serialPortsThread = threading.Thread(target=self._runSerialReader)
    self._serialPortsThread.setDaemon(True)
    
  def measurements(self):
    print("ProbeSerialReader.measurements()", file=sys.stderr)
    return (self._ec, self._ph)

  def _readline(self, serialPort): # (*)
#      print("ProbeSerialReader._readline()", file=sys.stderr)
      eol = b'\r'
      leneol = len(eol)
      line = bytearray()
      while True:
          c = serialPort.read(1)
          if c:
              line += c
              if line[-leneol:] == eol:
                  break
          else:
              break
      return bytes(line)

  def _runSerialReader(self):
#    print("ProbeSerialReader._runSerialReader()", file=sys.stderr)
    while True:
        ec = self._readline(self._ec_port)
        ph = self._readline(self._ph_port)
        if ec:
            self._ec = ec
        if ph:
            self._ph = ph

  def Start(self):
      print("ProbeSerialReader.Start()", file=sys.stderr)
      self._serialPortsThread.start()
      #_serialPortsThread.join()

# (*): The function node takes only one parameter, but is located in a class. Given the implicit class instance and your parameter, that's 2 arguments. To fix it, you can edit the function to
#      def _readline(self, serialPort):
# See for further details: https://stackoverflow.com/questions/31620212/why-does-this-error-say-im-giving-the-function-two-arguments
