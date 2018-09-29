"""Defines the LoadCellsReader class."""
import threading
import device_manager as DeviceManager

class LoadCellsReader(object):
    """Handles interaction with the load cells using a unique amplifier+ADC."""

    def __init__(self, calibration_factor=1):
        self._adc_output = 0
        self._calibration_factor = calibration_factor
        self._weight_gr = 0
    
    def configure_thread(self, cells):
        self._load_cells_thread = threading.Thread(target=self._run_adc_reader, args=(cells,)) #See (0) especially, (1), (2) and (3) below. Use kwargs, not args.
        self._load_cells_thread.setDaemon(True)

    def start(self):
        """Starts the background thread to get measurements from the load cells."""
        self._load_cells_thread.start()

    def weight_measurement(self):
        """Returns the weight measured."""
        return self._weight_gr

    def _run_adc_reader(self, cells):
        """Method that will be executed in every thread loop."""
        while True:
            self._adc_output = cells.get_weight(5) #5 is the amount of measurements that are averaged. The library has a default of 3.
            #print(str(self._adc_output))
            self._weight_gr = self._adc_output / self._calibration_factor #It is important to keep track of true weight at this point so that weight measurements from different times, or old, are not added together.

#(0): threading.Thread class needs an iterable of arguments as the args parameter. You're passing args=(threadnum) which is a single int object, you need to pass some iterable object that would allow multiple args, even when you only want to pass one arg. Link: https://stackoverflow.com/questions/49947814/python-threading-error-must-be-an-iterable-not-int
#(1): https://stackoverflow.com/questions/30273596/how-to-pass-list-to-python-worker-thread
#(2): https://stackoverflow.com/questions/30913201/pass-keyword-arguments-to-target-function-in-python-threading-thread
#(3): https://pythontips.com/2013/08/04/args-and-kwargs-in-python-explained/
        

