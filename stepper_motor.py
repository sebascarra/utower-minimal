"""Defines the PeristalticPump class."""
import device_manager as DeviceManager


class StepperMotor(object):
    """Models a peristaltic pump object, allowing to start and top it."""

    def __init__(self):
        self._is_on = False

    def start(self, dir_forward=True):
        """Starts the stepper motor in the specified direction.

        Args:
            dir_forward (bool, optional): Whether the stepper motor should be moved in
                the forward direction. Defaults to True.
        """
        DeviceManager.start_motor(dir_forward)
        self._is_on = True

    def stop(self):
        """Stops the stepper motor."""
        DeviceManager.stop_motor()
        self._is_on = False


