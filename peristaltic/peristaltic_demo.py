#!/usr/bin/env python

from time import sleep
import sys
import device_manager as DeviceManager

#Correct usage:
# -ComputerBoard knows what platform is being used and its physical characteristics.
# -DeviceManager knows the type and quantity of actuators used, and to what "pins" they are connected on the specific platform in use (but it does NOT know what the platform is, it only knows that it has "pins")
# -DeviceManager may use a real physical ComputerBoard or a "mock" simulated one.
# -Since DeviceManager knows the type, quantity and name of actuators/sensors, there is no option other than to initialize all actuators and sensors through DeviceManager methods.
# -Other than initializing sensors/actuators and freeing up resources, the attributes and methods related to sensors/actuators to be used have to be in the specific module of that sensor/actuator.

#Example:

def main(argv):

  DeviceManager.Init() #This is mandatory to use any of the available peristaltic pumps. Pump objects are created during the initialization of the DeviceManager.
  
  pump_name = argv[1] #The name of the pump to be tested is received as an argument.
  try:
    pump = DeviceManager.pumps[pump_name] #Get pump object for the pump to be tested. 
  except KeyError as e:
    print('Pump [{}] does not exist.'.format(pump_name))
    raise

  print('Starting motor sequence!')  
  while True:
    try:
      pump.Start(dir_forward=True) #From this point on we use exclusively functions inside the pump class, NOT the DeviceManager module.
      sleep(3)
      pump.Stop()
      sleep(1)
      pump.Start(dir_forward=False)
      sleep(3)
      pump.Stop()
      sleep(1)
    except(KeyboardInterrupt):
      # If a keyboard interrupt is detected then it exits cleanly!
      pump.Stop()
      print('Finishing up!')
    finally: #Freeing up resources is done through the device manager as it is the one that knows what pumps exist.
      DeviceManager.CleanFinalize() #This ensures a clean exit.
      quit()

if __name__ == "__main__":
  main(sys.argv)
