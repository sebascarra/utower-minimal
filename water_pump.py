import sys
import device_manager as DeviceManager

class WaterPump(object):

  def __init__(self):
    self._name = 'WP'
    self._is_on = False

  @property
  def name(self):
    return self._name
    
  def Start(self):
    DeviceManager.StartPump(self)
    self._is_on = True

  def Stop(self):
    DeviceManager.StopPump(self)
    self._is_on = False


