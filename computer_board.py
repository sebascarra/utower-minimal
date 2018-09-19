import RPi.GPIO as GPIO
import serial
import threading

def Init():
  GPIO.setmode(GPIO.BCM)

def SetOutputToPin(pin_number, state):
  GPIO.output(pin_number, state)

def InitializePinAsOutput(pin_number):
  GPIO.setup(pin_number, GPIO.OUT)

def CleanFinalize():
  GPIO.cleanup()


class ProbeSerialReader(object):
  #Original code: https://stackoverflow.com/questions/39176985/how-to-pipe-data-from-dev-ttyusb0-to-a-python-script
  #For custom readline definition See: https://stackoverflow.com/questions/16470903/pyserial-2-6-specify-end-of-line-in-readline

  def __init__(self, ec_port, ph_port):
    self._ec = 0.00
    self._ph = 0.00
    self._ec_port = serial.Serial(ec_port, 9600)
    self._ph_port = serial.Serial(ph_port, 9600)
    self._serialPortsThread = threading.Thread(target=self._serialReader)
    self._serialPortsThread.setDaemon(True)
    
  def measurements(self):
    return (self._ec, self._ph)

  def _readline(self, serialPort): # (*)
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

  def _serialReader(self):
    while True:
        ec = self._readline(self._ec_port)
        ph = self._readline(self._ph_port)
        if ec:
            self._ec = float(ec)
        if ph:
            self._ph = float(ph)

  def Init(self):
      self._serialPortsThread.start()
      #_serialPortsThread.join()

# (*): The function node takes only one parameter, but is located in a class. Given the implicit class instance and your parameter, that's 2 arguments. To fix it, you can edit the function to
#      def _readline(self, serialPort):
# See for further details: https://stackoverflow.com/questions/31620212/why-does-this-error-say-im-giving-the-function-two-arguments