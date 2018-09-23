"""Contains all code that interacts directly with the computer board hardware."""
from __future__ import print_function
import threading
import sys


def init():
    """Initializes the required pins and configuration for the board."""
    print('GPIO.setmode(GPIO.BCM)')


def set_output_to_pin(pin_number, state):
    """Sets the output of the given pin to the given state."""
    print(
        'GPIO.output({pin_number}, {state})'
        .format(pin_number=pin_number, state=state)
    )


def initialize_pin_as_output(pin_number):
    """Sets the given pin number as an output."""
    print(
        'GPIO.setup({pin_number}, GPIO.OUT)'
        .format(pin_number=pin_number)
    )


def clean_finalize():
    """Performs required cleanup before exiting the application."""
    print(
        'GPIO.cleanup()'
    )


class MockSerial(object):
    """Mocks the Serial class."""

    def __init__(self, port, rate):
        print("MockSerial.__init__()", file=sys.stderr)
        self._port = port
        self._rate = rate

    @staticmethod
    def read(_):
        """Mocks the serial read function."""
#        print("MockSerial.read()", file=sys.stderr)
        return "0.0\r"


class ProbeSerialReader(object):
    """Handles interaction with the probes via serial port."""

    def __init__(self, ec_port, ph_port):
        print("ProbeSerialReader.__init__()", file=sys.stderr)
        self._ec = 0.00
        self._ph = 0.00
        self._ec_port = MockSerial(ec_port, 9600)
        self._ph_port = MockSerial(ph_port, 9600)
        self._serial_ports_thread = threading.Thread(target=self._run_serial_reader)
        self._serial_ports_thread.setDaemon(True)

    def start(self):
        """Starts the background thread to get measurements from the serial port."""
        print("ProbeSerialReader.Start()", file=sys.stderr)
        self._serial_ports_thread.start()

    def measurements(self):
        """Returns the measured values of EC and PH."""
        print("ProbeSerialReader.measurements()", file=sys.stderr)
        return (self._ec, self._ph)

    @staticmethod
    def _read_line(serial_port):
        """Reads a line from the specified serial port."""
#        print("ProbeSerialReader._readline()", file=sys.stderr)
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
#        print("ProbeSerialReader._runSerialReader()", file=sys.stderr)
        while True:
            ec = self._read_line(self._ec_port)
            ph = self._read_line(self._ph_port)
            if ec:
                self._ec = float(ec)
            if ph:
                self._ph = float(ph)

