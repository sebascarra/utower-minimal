import RPi.GPIO as GPIO


def Init():
  GPIO.setmode(GPIO.BCM)


def SetOutputToPin(pin_number, state):
  GPIO.output(pin_number, state)


def InitializePinAsOutput(pin_number):
  GPIO.setup(pin_number, GPIO.OUT)


