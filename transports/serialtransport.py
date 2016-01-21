import serial

class SerialTransport:
    def __init__(self):
        self.driver = None

    def connect(self, options):
        print(options['port'])
        self.driver = serial.Serial(port=options['port'],baudrate=options['baudrate'])

    def disconnect(self):
        self.driver.close()

# The transport interface
    def read(self, maxbytes=1):
        in_waiting = self.driver.in_waiting
        if in_waiting > maxbytes:
            in_waiting = maxbytes
        read = self.driver.read(size=in_waiting)
        return read

    def readable(self):
        return self.driver.in_waiting

    def write(self, data):
        self.driver.write(data)
        return 0

    def writeable(self):
        return 1
