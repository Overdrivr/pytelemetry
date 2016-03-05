import serial
from logging import getLogger

class SerialTransport:
    def __init__(self):
        self.driver = None
        self.log_rx = getLogger('telemetry.rx')

    def connect(self, options):
        self.driver = serial.Serial(port=options['port'],baudrate=options['baudrate'])

    def disconnect(self):
        self.driver.close()

# The transport interface
    def read(self, maxbytes=1):
        try:
            in_waiting = self.driver.in_waiting
        except serial.SerialException as e:
            self.log_rx.error("Caught Exception during read driver.in_waiting : %s" % e)
            return None

        if in_waiting > maxbytes:
            in_waiting = maxbytes
        try:
            read = self.driver.read(size=in_waiting)
        except serial.SerialException as e:
            self.log_rx.error("Caught Exception during transport read : %s" % e)
            return None

        return read

    def readable(self):
        try:
            in_waiting = self.driver.in_waiting
        except serial.SerialException as e:
            self.log_rx.error("Caught Exception during read driver.in_waiting : %s" % e)
            return 0
    
        return self.driver.in_waiting

    def write(self, data):
        self.driver.write(data)
        return 0

    def writeable(self):
        return 1
