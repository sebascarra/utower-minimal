#!/usr/bin/env python

# A program to control the movement of a single motor using the RTK MCB!
# Composed by The Raspberry Pi Guy to accompany his tutorial!

# Let's import the modules we will need!
from time import sleep
import RPi.GPIO as GPIO
import sys

pumpName = sys.argv[1]

# Next we setup the pins for use!
GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)

pumps = {'P1': (18, 25), #Dictionary
         'WP': (8, 8),
         'P2': (7, 12),
         'P3': (16, 20)
}

try:
  print('GPIOs: ' + str(pumps[pumpName]))

  pin1 = pumps[pumpName][0]
  pin2 = pumps[pumpName][1]
  
  GPIO.setup(pin1, GPIO.OUT)
  GPIO.setup(pin2, GPIO.OUT)

  GPIO.output(pin1, False)
  GPIO.output(pin2, False)

  print('Starting motor sequence!')

  while True:
    try:
      # Makes the motor spin one way for 3 seconds
      GPIO.output(pin1, True)
      GPIO.output(pin2, False)
      sleep(3)
      # Idle for a sec
      GPIO.output(pin1, False)
      GPIO.output(pin2, False)
      sleep(1)
      # Spins the other way for a further 3 seconds
      GPIO.output(pin1, False)
      GPIO.output(pin2, True)
      sleep(3)
      # Idle for a sec
      GPIO.output(pin1, False)
      GPIO.output(pin2, False)
      sleep(1)
    except(KeyboardInterrupt):
      # If a keyboard interrupt is detected then it exits cleanly!
      print('Finishing up!')
      GPIO.output(pin1, False)
      GPIO.output(pin2, False)
      quit()
except:
  print('Pump does not exist.')


