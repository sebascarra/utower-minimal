import sys
import device_manager as DeviceManager

class ecPhProbes(object):

  def __init__(self):
    self._ec = 0.00
    self._ph = 0.00

  def getMeasurements(self):
    (ec, ph) = DeviceManager.updateMeasurements()
    self._ec = ec
    self._ph = ph
    return (self._ec, self._ph)

