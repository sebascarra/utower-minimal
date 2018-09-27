"""Defines the LoadCellsReader class."""
import threading
import device_manager as DeviceManager

class LoadCellsReader(object):
    """Handles interaction with the load cells."""

    def __init__(self, calibration_factor=1):
        self._cell_outputs = [0, 0, 0, 0]
        self._calibration_factor = calibration_factor
        self._weight_gr = 0
    
    def configure_thread(self, cells):
        self._load_cells_thread = threading.Thread(target=self._run_load_cell_reader, args=(cells,)) #See (1), (2) and (3) below. Use kwargs, not args.
        self._load_cells_thread.setDaemon(True)

    def start(self):
        """Starts the background thread to get measurements from the load cells."""
        self._load_cells_thread.start()

    def weight_measurement(self):
        """Returns the weight measured."""
        return self._weight_gr

    def _run_load_cell_reader(self, cells):
        """Method that will be executed in every thread loop."""
        while True:
            for i in range(0, 4):
                self._cell_outputs[i] = cells[i].get_weight(5) #5 is the amount of measurements that are averaged. The library has a default of 3.
                #print(str(self._cell_outputs[i]))
            #print("    ")
            self._weight_gr = sum(self._cell_outputs) / self._calibration_factor #It is important to keep track of true weight at this point so that weight measurements from different times, or old, are not added together.

#(1): https://stackoverflow.com/questions/30273596/how-to-pass-list-to-python-worker-thread
#(2): https://stackoverflow.com/questions/30913201/pass-keyword-arguments-to-target-function-in-python-threading-thread
#(3): https://pythontips.com/2013/08/04/args-and-kwargs-in-python-explained/
        

