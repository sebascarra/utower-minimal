"""Handles the device, acting as a proxy between the application and the computer board."""
import computer_board as ComputerBoard
#import mock_computer_board as ComputerBoard
from peristaltic_pump import PeristalticPump
from water_pump import WaterPump
from probes_module import EcPhProbes
from probe_serial_reader import ProbeSerialReader
from solenoid_valve import SolenoidValve



#Initialize board pins to be used by hardware components.
ComputerBoard.init()

#Set up hardware components: #################################################

#Peristaltic pumps:
PERISTALTIC_PINS = {
    'P1': (18, 25),
    'P2': (27, 12),
    'P3': (16, 20)
}

peristaltic_pumps = {}

#Water pump:
WATER_PUMP_PIN = 22

water_pump = None #For cleaniness, this is set to an initial value during Init().

#EC and pH probes:
EC_ATLAS_PORT = '/dev/serial0'
PH_ATLAS_PORT = '/dev/ttyUSB0'

probes = None #Thread is going to be started during Init().
serial_reader = ProbeSerialReader(
    ComputerBoard.create_serial(EC_ATLAS_PORT, 9600),
    ComputerBoard.create_serial(PH_ATLAS_PORT, 9600)
)

#Solenoid valve
SOLENOID_VALVE_PIN = 17

solenoid_valve = None #For cleaniness, this is set to an initial value during Init().

#Load cells:

"""CELL_DT_PINS = (10, 5, 13, 26)"""
"""CELL_SCK_PINS = (9, 6, 19, 21)"""

CELL_PINS = {
    'C1': (10, 9),
    'C2': (5, 6),
    'C3': (13, 19),
    'C4': (26, 21)
}

hxs = []

#End of setup of hardware components #########################################

def init():
    """Initializes the device manager, creating the required objects."""
    #Initialize peristaltic pumps:
    for pump_name in PERISTALTIC_PINS:
        pump = PeristalticPump(pump_name)
        peristaltic_pumps[pump_name] = pump # -> Why we don't need to use the "global" keyword here: https://stackoverflow.com/questions/14323817/global-dictionaries-dont-need-keyword-global-to-modify-them
        pin1, pin2 = _peristaltic_pins_from_name(pump_name)
        ComputerBoard.initialize_pin_as_output(pin1)
        ComputerBoard.initialize_pin_as_output(pin2)
        pump.stop()
    #Initialize water pump:
    global water_pump #See (*) at bottom.
    water_pump = WaterPump()
    ComputerBoard.initialize_pin_as_output(WATER_PUMP_PIN)
    water_pump.stop()
    #Initialize EC and PH probes:
    global probes
    probes = EcPhProbes()
    serial_reader.start()
    probes.get_measurements()
    #Initialize solenoid valve:
    global solenoid_valve
    solenoid_valve = SolenoidValve()
    ComputerBoard.initialize_pin_as_output(SOLENOID_VALVE_PIN)
    solenoid_valve.close()
    #Initialize load cells:
    for cell_name in CELL_PINS:
        hx = HX711(dtPins[i], sckPins[i])
        hx.set_reading_format("LSB", "MSB")
        #hx.set_reference_unit(113)
        hx.reset()
        hx.tare()
        hxs.append(hx)
        

#Auxiliary functions: ########################################################

  #For peristaltic pumps:

def start_pump(pump, dir_forward=True):
    """Starts a pump."""
    if pump.name != 'WP':
        #Procedure for peristaltics:
        pin1, pin2 = _peristaltic_pins_from_name(pump.name)
        ComputerBoard.set_output_to_pin(pin1, not dir_forward)
        ComputerBoard.set_output_to_pin(pin2, dir_forward)
        #Procedure for water pump:
    else:
        ComputerBoard.set_output_to_pin(WATER_PUMP_PIN, True)


def stop_pump(pump):
    """Stops a pump."""
    if pump.name != 'WP':
        #Procedure for peristaltics:
        pin1, pin2 = _peristaltic_pins_from_name(pump.name)
        ComputerBoard.set_output_to_pin(pin1, False)
        ComputerBoard.set_output_to_pin(pin2, False)
    else:
        #Procedure for water pump:
        ComputerBoard.set_output_to_pin(WATER_PUMP_PIN, False)


def stop_all_pumps():
    """Stops all the pumps in the device."""
    #Procedure for peristaltics:
    for pump in peristaltic_pumps.values():
        pump.stop()
    #Procedure for water pump:
    water_pump.stop()


def _peristaltic_pins_from_name(pump_name):
    """Returs the pins corresponding to a pump."""
    pin1 = PERISTALTIC_PINS[pump_name][0]
    pin2 = PERISTALTIC_PINS[pump_name][1]
    return pin1, pin2


  #For EC and pH probes:


def get_measurements():
    """Returns the EC and PH measurements."""
    return serial_reader.measurements()


  #For solenoid valve:

def open_valve():
    """Opens the solenoid valve in the device."""
    ComputerBoard.set_output_to_pin(SOLENOID_VALVE_PIN, True)

def close_valve():
    """Shuts/closes the solenoid valve in the device."""
    ComputerBoard.set_output_to_pin(SOLENOID_VALVE_PIN, False)

#End of auxiliary functions. ###################################################


def clean_finalize():
    """Performs required cleanup before exiting the application."""
    ComputerBoard.clean_finalize()

#(*):

# From: https://stackoverflow.com/questions/10588317/python-function-global-variables
# 303
# down vote
# accepted
# If you want to simply access a global variable you just use its name. However to change its value you need to use the global keyword.
# E.g.
# global someVar
# someVar = 55
# This would change the value of the global variable to 55. Otherwise it would just assign 55 to a local variable.

# 75
# down vote
# Within a Python scope, any assignment to a variable not already declared within that scope creates a new local variable unless that variable is declared earlier in the function as referring to a globally scoped variable with the keyword global.
