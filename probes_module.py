"""Defines the EcPhProbe class."""
import device_manager as DeviceManager


class EcPhProbes(object):
    """Models the EC and PH probes, allowing to get the corresponding measurements."""

    def __init__(self):
        self._ec = 0.0
        self._ph = 0.0

    def get_measurements(self):
        """Returns the EC and PH values.

        Returns:
            (tuple): tuple containing:
                ec (float): The value of EC measured.
                ph (float): The value of PH measured.
        """
        (ec, ph) = DeviceManager.get_measurements()
        self._ec = ec
        self._ph = ph
        return (self._ec, self._ph)

