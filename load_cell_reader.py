"""Defines the LoadCellReader class."""
import threading
import device_manager as DeviceManager

class LoadCellReader(object):
    """Handles interaction with the load cells."""

    def __init__(self, calibration_factor, cells):
        self._cell_outputs = (0, 0, 0, 0)
        self._calibration_factor = calibration_factor
        self._weight_gr = 0
        self._load_cells_thread = threading.Thread(target=self._run_load_cell_reader, args=cells)
        self._load_cells_thread.setDaemon(True)

    def start(self):
        """Starts the background thread to get measurements from the load cells."""
        self._load_cells_thread.start()

    def weight_measurement(self):
        """Returns the weight measured."""
        return ((self._c1 + self._c2 + self._c3 + self._c4) / self._calibration_factor ) #TODO: determine if relationship is linear.

    def _run_load_cell_reader(self, cells):
        """Method that will be executed in every thread loop."""
        while True:
            for i in range(0, 4):
            self._cell_outputs[i] = cells[i].get_weight(5)
            #print(str(i + 1) + ": " +  str(val), end=' // ')
            cells[i].power_down()
            cells[i].power_up()
            #print("")


        

