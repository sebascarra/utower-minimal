"""Contains all code that interacts directly with the computer board hardware."""
import serial
import RPi.GPIO as GPIO
from hx711 import HX711
from time import sleep
import pigpio
import os

pi = None #This will be set during initialization.

def init():
    """Initializes the required pins and configuration for the board. Starts the pigpio daemon for those modules that use pigpio instead of RPi.GPIO, and connects this application to it."""
    GPIO.setmode(GPIO.BCM)
    #os.system('sudo pigpiod')
    global pi
    pi = pigpio.pi()


def set_output_to_pin(pin_number, state):
    """Sets the output of the given pin to the given state for a pin that runs using RPi.GPIO."""
    GPIO.output(pin_number, state)

def set_output_to_pin_pigpio(pin_number, state):
    """Sets the output of the given pin to the given state for a pin that runs using pigpio."""
    pi.write(pin_number, state)


def initialize_pin_as_output(pin_number):
    """Sets the given pin number as an output for a pin that runs using RPi.GPIO."""
    GPIO.setup(pin_number, GPIO.OUT)

def initialize_pin_as_output_pigpio(pin_number):
    """Sets the given pin number as an output for a pin that runs using pigpio."""
    pi.set_mode(pin_number, pigpio.OUTPUT)


def clean_finalize():
    """Performs required cleanups before exiting the application."""
    GPIO.cleanup()
    pi.stop()

#For EC and pH probes:

def create_serial(port, rate):
    """Creates a new Serial object at the given port with the given rate."""
    return serial.Serial(port, rate)

#For load cells:

def initialize_adc_in_pins(dt_pin, sck_pin):
    """Creates a new load cell ADC object at the given pins."""
    hx = HX711(dt_pin, sck_pin)
    hx.set_reading_format("LSB", "MSB")
    hx.power_down()
    sleep(1) #Such long delays are added because of a 400 ms establishing time specified by the datasheet of the HX711.
    hx.power_up()
    sleep(1)
    hx.tare()
    return hx

#For stepper motor:

def start_pigpio_daemon():
    """Starts the pigpio daemon and connects this application to it."""
    os.system('sudo pigpiod')
    pi = pigpio.pi()
    return pi

def set_pwm_on(pin, frequency=100, duty_cycle=128):
    pi.set_PWM_dutycycle(pin, duty_cycle)
    pi.set_PWM_frequency(pin, frequency)

def set_pwm_off(pin):
    pi.set_PWM_dutycycle(pin, 0)

    

