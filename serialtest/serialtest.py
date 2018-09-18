import serial

#Original code: https://stackoverflow.com/questions/39176985/how-to-pipe-data-from-dev-ttyusb0-to-a-python-script
#For custom readline definition See: https://stackoverflow.com/questions/16470903/pyserial-2-6-specify-end-of-line-in-readline



def _readline():
    eol = b'\r'
    leneol = len(eol)
    line = bytearray()
    while True:
        c = ser.read(1)
        if c:
            line += c
            if line[-leneol:] == eol:
                break
        else:
            break
    return bytes(line)

#ser = serial.Serial('/dev/ttyUSB0', 9600)
ser = serial.Serial('/dev/serial0', 9600)

while True:
    data = _readline()
    if data:
        print(data)
