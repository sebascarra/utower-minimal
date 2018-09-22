import serial
import threading

#Original code: https://stackoverflow.com/questions/39176985/how-to-pipe-data-from-dev-ttyusb0-to-a-python-script
#For custom readline definition See: https://stackoverflow.com/questions/16470903/pyserial-2-6-specify-end-of-line-in-readline

def _readline(serialPort):
    eol = b'\r'
    leneol = len(eol)
    line = bytearray()
    while True:
        c = serialPort.read(1)
        if c:
            line += c
            if line[-leneol:] == eol:
                break
        else:
            break
    return bytes(line)

def serialReader():
    serPH = serial.Serial('/dev/ttyUSB0', 9600)
    serEC = serial.Serial('/dev/serial0', 9600)
    while True:
        pH = _readline(serPH)
        EC = _readline(serEC)

        if pH:
            print "pH: ", pH, "\n"
        if EC:
            print "EC: ", EC, "\n"

def main():
    serialPortsThread = threading.Thread(target=serialReader)
    serialPortsThread.setDaemon(True)
    serialPortsThread.start()
    serialPortsThread.join()

if __name__ == "__main__":
  main()
