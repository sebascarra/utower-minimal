import device_manager as DeviceManager

class WaterPump(object):

  def __init__(self):
    self._is_on = False
    
  def Start(dir_forward=True):
    DeviceManager.StartPump(self)
    self._is_on = True

  def Stop():
    DeviceManager.StopPump(self)
    self._is_on = False


