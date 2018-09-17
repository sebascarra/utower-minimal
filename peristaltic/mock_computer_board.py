def Init():
  print('GPIO.setmode(GPIO.BCM)')


def SetOutputToPin(pin_number, state):
  print(
    'GPIO.output({pin_number}, {state})'
    .format(pin_number=pin_number, state=state)
  )


def InitializePinAsOutput(pin_number):
  print(
    'GPIO.setup({pin_number}, GPIO.OUT)'
    .format(pin_number=pin_number)
  )


