from  .. import pytelemetry
import queue
import mock

class transportMock:
    def __init__(self):
        self.queue = queue.Queue()
    def read(self, maxbytes=1):
        data = []
        amount = 0
        print("Requested ",maxbytes)
        while amount < maxbytes and not self.queue.empty():
            c = self.queue.get()
            print("Reading :",c)
            data.append(c)
            amount += 1
        return data

    def readable(self):
        return self.queue.qsize()

    def write(self, data):
        for i in range(len(data)):
            print("Writing :",data[i])
            self.queue.put(data[i])
        return 0

    def writeable(self):
        return not self.queue.full()

def test_publish():
    # Setup
    t = transportMock()
    c = pytelemetry.pytelemetry(t)
    cb = mock.Mock(spec=["topic","data"])
    default_cb = mock.Mock(spec=["topic","data"])
    c.subscribe('sometopic',cb)
    c.subscribe(None,default_cb)

    # testing
    assert t.queue.qsize() == 0
    # Writing to mock transport is looped back to read
    c.publish(b'sometopic',b'booyaa','string')
    assert t.queue.qsize() > 0
    c.update()
    assert t.queue.qsize() == 0
    cb.assert_called_once_with('sometopic',b'booyaa')
    #cb.assert_called_once_with('othertopic',b'booyaa')
