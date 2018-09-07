#!/usr/bin/env python

# A program to control the movement of a single motor using the RTK MCB!
# Composed by The Raspberry Pi Guy to accompany his tutorial!

# Let's import the modules we will need!
import time
import RPi.GPIO as GPIO

# Next we setup the pins for use!
GPIO.setmode(GPIO.BCM)

GPIO.setup(17,GPIO.OUT)

GPIO.output(17,False)

# print('Starting motor sequence!')

while True:
  try:
    # Makes the motor spin one way for 3 seconds
    GPIO.output(17, True)
    time.sleep(3)
    # Spins the other way for a further 3 seconds
    GPIO.output(17, False)
    time.sleep(3)
  except(KeyboardInterrupt):
    # If a keyboard interrupt is detected then it exits cleanly!
    print('Finishing up!')
    GPIO.output(17, False)
    quit()
