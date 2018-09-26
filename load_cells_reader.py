"""Defines the LoadCellsReader class."""
import threading
import device_manager as DeviceManager

class LoadCellsReader(object):
    """Handles interaction with the load cells."""

    def __init__(self, calibration_factor):
        self._cell_outputs = (0, 0, 0, 0)
        self._calibration_factor = calibration_factor
        self._weight_gr = 0
    
    def configure_thread(self, cells):
        self._load_cells_thread = threading.Thread(target=self._run_load_cell_reader, args=cells)
        self._load_cells_thread.setDaemon(True)

    def start(self):
        """Starts the background thread to get measurements from the load cells."""
        self._load_cells_thread.start()

    def weight_measurement(self):
        """Returns the weight measured."""
        return ( self._cell_outputs[1] + self._cell_outputs[2] + self._cell_outputs[3] + self._cell_outputs[4] / self._calibration_factor ) #TODO: determine if relationship is linear.

    def _run_load_cell_reader(self, cells):
        """Method that will be executed in every thread loop."""
        while True:
            for i in range(0, 4):
                self._cell_outputs[i] = cells[i].get_weight(5)
                #print(str(i + 1) + ": " +  str(val), end=' // ')
                cells[i].power_down()
                cells[i].power_up()
                #print("")


        

