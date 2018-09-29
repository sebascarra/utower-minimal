"""Contains all code that interacts directly with the computer board hardware."""
from __future__ import print_function
from time import sleep
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

#For EC and pH probes:

def create_serial(port, rate):
    """Creates a new Serial object at the given port with the given rate."""
    return MockSerial(port, rate)

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

#For load cells:

def initialize_cell_in_pins(dt_pin, sck_pin):
    print(
        'hx = HX711({dt_pin}}, {sck_pin})'
        .format(dt_pin=dt_pin, sck_pin=sck_pin)
    )

    hx = MockHX711(dt_pin, sck_pin)
    return hx

class MockHX711(object):
    """Mocks the HX711 class."""

    def __init__(self, dt_pin, sck_pin):
        print("HX711.__init__()", file=sys.stderr)
        self._dt_pin = dt_pin
        self._sck_pin = sck_pin

    @staticmethod
    def get_weight(_):
        """Mocks the HX711 get_weight function."""
        return "123"

    @staticmethod
    def power_down(_):
        """Mocks the HX711 power_down function."""
        sleep(0.5)

    @staticmethod
    def power_up(_):
        """Mocks the HX711 power_up function."""
        sleep(0.5)