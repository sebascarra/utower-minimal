import device_manager as DeviceManager

class PeristalticPump(object):

  def __init__(self, name):
    self._name = name
    self._is_on = False

  @property
  def name(self):
    return self._name
    
  def Start(self, dir_forward=True):
    DeviceManager.StartPump(self, dir_forward)
    self._is_on = True

  def Stop(self):
    DeviceManager.StopPump(self)
    self._is_on = False


