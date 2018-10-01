"""Contains all code that interacts directly with the computer board hardware."""
import serial
import RPi.GPIO as GPIO
from hx711 import HX711
from time import sleep
import pigpio
import os
import glob

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

def initialize_pin_as_input_with_pull_up(pin_number):
    """Sets the given pin number as an input, along with an internal pull-up resistor, for a pin that runs using RPi.GPIO."""
    GPIO.setup(pin_number, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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

#For DS18B20 thermometer sensor:
    
class DS18B20(object):

    def __init__(self):
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        self._base_dir = '/sys/bus/w1/devices/'
        self._device_folder = glob.glob(self._base_dir + '28*')[0]
        self._device_file = self._device_folder + '/w1_slave'
    
    def _read_temp_raw(self):
        f = open(self._device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines
 
    def read_temp(self):
        lines = self._read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            sleep(0.2)
            lines = self._read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            #return temp_c, temp_f
            return temp_c



