import serial
from logging import getLogger

class SerialTransport:
    def __init__(self):
        self.driver = None
        self.log_tr = getLogger('telemetry.transport.serial')
        self.log_tr.info("SerialTransport initialized.")

        self.resetStats()

    def resetStats(self, averaging_window=100):
        # Construct a dictionnary for holding references to all counters
        self.measurements = {
            "rx_bytes"  : 0, # To store amount of received and sent characters
            "tx_bytes"  : 0,
            "rx_chunks" : 0, # To store amount of chunks of data
            "tx_chunks"  : 0,
            "rx_in_waiting" : 0, # To store current, avg and peak RX queue size
            "rx_in_waiting_avg" : 0,
            "rx_in_waiting_max" : 0
        }
        self.averaging_window = averaging_window

    def stats(self):
        return self.measurements

    def connect(self, options):
        # Default values for options for retrocompatibility
        if not 'timeout' in options:
            options['timeout'] = 1
        self.driver = serial.Serial(port=options['port'],
                                    baudrate=options['baudrate'],
                                    write_timeout=options['timeout'])

    def disconnect(self):
        self.driver.close()

    def read(self, maxbytes=1):
        try:
            in_waiting = self.driver.in_waiting
        except serial.SerialException as e:
            self.log_tr.error("Caught Exception during read driver.in_waiting : %s" % e)
            return None

        if in_waiting > maxbytes:
            in_waiting = maxbytes

        try:
            bytesread = self.driver.read(size=in_waiting)
        except serial.SerialException as e:
            self.log_tr.error("Caught Exception during transport read : %s" % e)
            return None

        self.measurements['rx_bytes'] += len(bytesread)
        self.measurements['rx_chunks'] += 1

        return bytesread

    def readable(self):
        try:
            in_waiting = self.driver.in_waiting
        except serial.SerialException as e:
            self.log_tr.error("Caught Exception during read driver.in_waiting : %s" % e)
            return 0

        self.measurements['rx_in_waiting'] = in_waiting
        self.measurements['rx_in_waiting_max'] = max(self.measurements['rx_in_waiting_max'], in_waiting)
        self.measurements['rx_in_waiting_avg'] = (in_waiting + self.averaging_window * self.measurements['rx_in_waiting_avg']) / (self.averaging_window + 1)

        return in_waiting

    def write(self, data):
        self.driver.write(data)
        self.measurements['tx_bytes'] += len(data)
        self.measurements['tx_chunks'] += 1
        return 0

    def writeable(self):
        return 1
