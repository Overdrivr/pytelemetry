import serial
from logging import getLogger

class SerialTransport:
    def __init__(self):
        self.driver = None
        self.log_tr = getLogger('telemetry.transport.serial')
        self.log_rx_queue = getLogger('telemetry.transport.serial.rxqueue')
        self.log_rx_chunks = getLogger('telemetry.transport.serial.rxchunks')
        self.log_tx_chunks = getLogger('telemetry.transport.serial.txchunks')
        self.log_tr.info("SerialTransport initialized.")

        self.resetStats()

    def resetStats(self):
        # To store amount of received and sent characters.
        self.rx_bytes_count = 0
        self.tx_bytes_count = 0
        # To store amount of chunks of data
        self.rx_chunks_count = 0
        self.tx_chunks_count = 0

    def stats(self):
        return {
            "rx_bytes"  : self.rx_bytes_count,
            "tx_bytes"  : self.tx_bytes_count,
            "rx_chunks" : self.rx_chunks_count,
            "tx_chunks"  : self.tx_chunks_count
        }

    def connect(self, options):
        # Default values for options for retrocompatibility
        if not 'timeout' in options:
            options['timeout'] = 1
        self.driver = serial.Serial(port=options['port'],
                                    baudrate=options['baudrate'],
                                    write_timeout=options['timeout'])

    def disconnect(self):
        self.driver.close()

# The transport interface
    def read(self, maxbytes=1):
        try:
            in_waiting = self.driver.in_waiting
        except serial.SerialException as e:
            self.log_tr.error("Caught Exception during read driver.in_waiting : %s" % e)
            return None

        self.log_rx_queue.debug('processing / available bytes : %s / %s' % (in_waiting, maxbytes))
        if in_waiting > maxbytes:
            in_waiting = maxbytes

        try:
            bytesread = self.driver.read(size=in_waiting)
        except serial.SerialException as e:
            self.log_tr.error("Caught Exception during transport read : %s" % e)
            return None

        self.rx_bytes_count += len(bytesread)
        self.rx_chunks_count += 1
        self.log_rx_chunks.debug(str(bytesread))

        return bytesread

    def readable(self):
        try:
            in_waiting = self.driver.in_waiting
        except serial.SerialException as e:
            self.log_tr.error("Caught Exception during read driver.in_waiting : %s" % e)
            return 0

        self.log_rx_queue.debug('available bytes : %s' % in_waiting)

        return in_waiting

    def write(self, data):
        self.driver.write(data)
        self.tx_bytes_count += len(data)
        self.tx_chunks_count += 1
        return 0

    def writeable(self):
        return 1
