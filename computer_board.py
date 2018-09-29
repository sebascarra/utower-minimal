"""Contains all code that interacts directly with the computer board hardware."""
import serial
import RPi.GPIO as GPIO
from hx711 import HX711
from time import sleep


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

#For EC and pH probes:

def create_serial(port, rate):
    """Creates a new Serial object at the given port with the given rate."""
    return serial.Serial(port, rate)

#For load cells:

def initialize_adc_in_pins(dt_pin, sck_pin):
    hx = HX711(dt_pin, sck_pin)
    hx.set_reading_format("LSB", "MSB")
    hx.power_down()
    sleep(1) #Such long delays are added because of a 400 ms establishing time specified by the datasheet of the HX711.
    hx.power_up()
    sleep(1)
    hx.tare()
    return hx

