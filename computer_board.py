"""Contains all code that interacts directly with the computer board hardware."""
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


def create_serial(port, rate):
    """Creates a new Serial object at the given port with the given rate."""
    return serial.Serial(port, rate)

