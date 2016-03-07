from pytelemetry import Pytelemetry
import queue
import unittest.mock as mock
from pytelemetry.transports.serialtransport import SerialTransport

class driverMock:
    def __init__(self):
        self.queue = queue.Queue()
        self.in_waiting = 0

    def read(self, size=1):
        data = []
        amount = 0
        while amount < size and not self.queue.empty():
            c = self.queue.get()
            data.append(c)
            self.in_waiting -= 1
            amount += 1
        return data

    def write(self, data):
        for i in range(len(data)):
            self.queue.put(data[i])
            self.in_waiting += 1
        return 0


def test_serial_stats():
    # Setup
    t = SerialTransport()
    t.driver = driverMock()
    c = Pytelemetry(t)

    stats = t.stats()

    assert stats['rx_bytes'] == 0
    assert stats['rx_chunks'] == 0
    assert stats['tx_bytes'] == 0
    assert stats['tx_chunks'] == 0

    c.publish('foo','bar','string')

    stats = t.stats()

    assert stats['rx_bytes'] == 0
    assert stats['rx_chunks'] == 0
    assert stats['tx_bytes'] == 13
    assert stats['tx_chunks'] == 1

    c.update()

    stats = t.stats()

    assert stats['rx_bytes'] == 13
    assert stats['rx_chunks'] == 13 # TODO : For now data read byte after byter. To replace by read in bulk
    assert stats['tx_bytes'] == 13
    assert stats['tx_chunks'] == 1

    c.publish('fooqux',-32767,'int16')

    stats = t.stats()

    assert stats['rx_bytes'] == 13
    assert stats['rx_chunks'] == 13
    assert stats['tx_bytes'] == 13 + 15
    assert stats['tx_chunks'] == 2

    c.update()

    stats = t.stats()

    assert stats['rx_bytes'] == 13 + 15
    assert stats['rx_chunks'] == 13 + 15
    assert stats['tx_bytes'] == 13 + 15
    assert stats['tx_chunks'] == 2

    t.resetStats()

    stats = t.stats()
    
    assert stats['rx_bytes'] == 0
    assert stats['rx_chunks'] == 0
    assert stats['tx_bytes'] == 0
    assert stats['tx_chunks'] == 0
