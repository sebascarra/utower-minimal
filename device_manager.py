"""Handles the device, acting as a proxy between the application and the computer board."""
import computer_board as ComputerBoard
#import mock_computer_board as ComputerBoard



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
#EC_ATLAS_PORT = '/dev/serial0'
#PH_ATLAS_PORT = '/dev/ttyUSB0'

# probes = None #Thread is going to be started during Init().
# serial_reader = ProbeSerialReader(
#     ComputerBoard.create_serial(EC_ATLAS_PORT, 9600),
#     ComputerBoard.create_serial(PH_ATLAS_PORT, 9600)
# )

#Solenoid valve
SOLENOID_VALVE_PIN = 17

solenoid_valve = None #For cleaniness, this is set to an initial value during Init().

#Load cells:
ADC_PINS = (10, 9) #DT, SCK

CALIBRATION_FACT0R = 1

adc = None #For cleaniness, this is set to an initial value during Init().
load_cells_object = None #For cleaniness, this is set to an initial value during Init().
cells_reader = None

#Stepper motor:
STEPPER_PINS = (23, 24) #STEP, DIR

stepper = None #For cleaniness, this is set to an initial value during Init().

#DS18B20 water thermometer:

# DS18B20_PIN = 4

# water_thermometer = None #For cleaniness, this is set to an initial value during Init().
# water_thermometer_reader = WaterThermometerReader()

#End of setup of hardware components #########################################

def init(device):
    """Initializes the device manager, creating the required objects."""
    if (device == "peristaltic_pump"):
        from peristaltic_pump import PeristalticPump
    if (device == "water_pump"):
        from water_pump import WaterPump
    #from probes_module import EcPhProbes
    #from probe_serial_reader import ProbeSerialReader
    if (device == "solenoid_valve"):
        from solenoid_valve import SolenoidValve
    if (device == "load_cells"):
        from load_cells import LoadCells
        from load_cells_reader import LoadCellsReader
    if (device == "stepper_motor"):
        from stepper_motor import StepperMotor
    #from water_thermometer import WaterThermometer
    #from water_thermometer_reader import WaterThermometerReader
    #Initialize board pins to be used by hardware components.
    ComputerBoard.init()
    #Initialize peristaltic pumps:
    if (device == "peristaltic_pump"):
        for pump_name in PERISTALTIC_PINS:
            pump = PeristalticPump(pump_name)
            peristaltic_pumps[pump_name] = pump # -> Why we don't need to use the "global" keyword here: https://stackoverflow.com/questions/14323817/global-dictionaries-dont-need-keyword-global-to-modify-them
            pin1, pin2 = _peristaltic_pins_from_name(pump_name)
            ComputerBoard.initialize_pin_as_output(pin1)
            ComputerBoard.initialize_pin_as_output(pin2)
            pump.stop()
    #Initialize water pump:
    if (device == "water_pump"):
        global water_pump #See (*) at bottom.
        water_pump = WaterPump()
        ComputerBoard.initialize_pin_as_output(WATER_PUMP_PIN)
        water_pump.stop()
    #Initialize EC and PH probes:
    # global probes
    # probes = EcPhProbes()
    # serial_reader.start()
    # probes.get_measurements()
    #Initialize solenoid valve:
    if (device == "solenoid_valve"):
        global solenoid_valve
        solenoid_valve = SolenoidValve()
        ComputerBoard.initialize_pin_as_output(SOLENOID_VALVE_PIN)
        solenoid_valve.close()
    #Initialize load cells:
    if (device == "load_cells"):
        global cells_reader
        cells_reader = LoadCellsReader(CALIBRATION_FACT0R)
        dt_pin, sck_pin = _adc_pins_from_name()
        global adc
        adc = ComputerBoard.initialize_adc_in_pins(dt_pin, sck_pin)
        cells_reader.configure_thread(adc)
        cells_reader.start()
        global load_cells_object
        load_cells_object = LoadCells()
    #Initialize stepper motor:
    if (device == "stepper_motor"):
        global stepper
        stepper = StepperMotor()
        stepper.stop()
    #Initialize DS18B20
    # ComputerBoard.initialize_pin_as_input_with_pull_up(DS18B20_PIN)
    # ds18b20_object = ComputerBoard.DS18B20()
    # water_thermometer_reader.configure_thread(ds18b20_object)
    # water_thermometer_reader.start()
    # global water_thermometer
    # water_thermometer = WaterThermometer()


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

  #For load cells:

def _adc_pins_from_name():
    """Returs the pins corresponding to a load cell ADC."""
    dt_pin = ADC_PINS[0]
    sck_pin = ADC_PINS[1]
    return dt_pin, sck_pin

def get_weight_measurement():
    """Returns the load cell weight measurements."""
    return cells_reader.weight_measurement()


  #For stepper motor:

def start_motor(direction, steps_per_second=1600):
    """Starts the stepper motor."""
    ComputerBoard.set_output_to_pin_pigpio(STEPPER_PINS[1], direction) #Set stepper direction.
    ComputerBoard.set_pwm_on(STEPPER_PINS[0], steps_per_second) #Set stepper steps per second.


def stop_motor():
    """Stops the stepper motor."""
    ComputerBoard.set_pwm_off(STEPPER_PINS[0]) #Set stepper steps per second to zero.


  #For water thermometer:

def get_temperature_measurement():
    return water_thermometer_reader.temp_measurement()
    

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
