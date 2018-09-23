"""Contains all code that interacts directly with the computer board hardware."""
from __future__ import print_function
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

