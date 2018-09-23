"""Contains all code that interacts directly with the computer board hardware."""
import threading
import serial
import RPi.GPIO as GPIO


def init():
    """Initializes the required pins and configuration for the board."""
    GPIO.setmode(GPIO.BCM)


def set_output_to_pin(pin_number, state):
    """Sets the output of the given pin to the given state."""
    GPIO.output(pin_number, state)


def initialize_pin_as_output(pin_number):
    """Sets the given pin number as an output."""
    GPIO.setup(pin_number, GPIO.OUT)


def clean_finalize():
    """Performs required cleanup before exiting the application."""
    GPIO.cleanup()


class ProbeSerialReader(object):
    """Handles interaction with the probes via serial port."""
  #Original code: https://stackoverflow.com/questions/39176985/how-to-pipe-data-from-dev-ttyusb0-to-a-python-script
  #For custom readline definition See: https://stackoverflow.com/questions/16470903/pyserial-2-6-specify-end-of-line-in-readline

    def __init__(self, ec_port, ph_port):
        self._ec = 0.00
        self._ph = 0.00
        self._ec_port = serial.Serial(ec_port, 9600)
        self._ph_port = serial.Serial(ph_port, 9600)
        self._serial_ports_thread = threading.Thread(target=self._run_serial_reader)
        self._serial_ports_thread.setDaemon(True)

    def start(self):
        """Starts the background thread to get measurements from the serial port."""
        self._serial_ports_thread.start()

    def measurements(self):
        """Returns the measured values of EC and PH."""
        return (self._ec, self._ph)

    @staticmethod
    def _read_line(serial_port):
        """Reads a line from the specified serial port."""
        eol = b'\r'
        leneol = len(eol)
        line = bytearray()
        while True:
            char = serial_port.read(1)
            if char:
                line += char
                if line[-leneol:] == eol:
                    break
            else:
                break
        return bytes(line)

    def _run_serial_reader(self):
        """method that will be executed in every thread loop."""
        while True:
            ec = self._read_line(self._ec_port)
            ph = self._read_line(self._ph_port)
            if ec:
                self._ec = float(ec)
            if ph:
                self._ph = float(ph)

