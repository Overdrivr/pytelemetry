from  ..pytelemetry import Pytelemetry
import queue
import unittest.mock as mock

class transportMock:
    def __init__(self):
        self.queue = queue.Queue()
    def read(self, maxbytes=1):
        data = []
        amount = 0
        while amount < maxbytes and not self.queue.empty():
            c = self.queue.get()
            data.append(c)
            amount += 1
        return data

    def readable(self):
        return self.queue.qsize()

    def write(self, data):
        for i in range(len(data)):
            self.queue.put(data[i])
        return 0

    def writeable(self):
        return not self.queue.full()

def test_end_to_end_string():
    # Setup
    t = transportMock()
    c = Pytelemetry(t)
    cb = mock.Mock(spec=["topic","data"])
    default_cb = mock.Mock(spec=["topic","data"])
    c.subscribe('sometopic',cb)
    c.subscribe(None,default_cb)

    # testing callback subscribed to topic
    assert t.queue.qsize() == 0
    c.publish('sometopic','someMessage','string')
    assert t.queue.qsize() > 0
    c.update()
    assert t.queue.qsize() == 0
    cb.assert_called_once_with('sometopic','someMessage')

    # test default callback
    c.publish('othertopic','otherMessage','string')
    assert t.queue.qsize() > 0
    c.update()
    assert t.queue.qsize() == 0
    default_cb.assert_called_once_with('othertopic','otherMessage')

def test_topic_contains_space_first():
    # Setup
    t = transportMock()
    c = Pytelemetry(t)
    cb = mock.Mock(spec=["topic","data"])
    c.subscribe(' topicwithspacefirst',cb)

    c.publish(' topicwithspacefirst',1234567,'int32')
    assert t.queue.qsize() > 0
    c.update()
    assert t.queue.qsize() == 0
    cb.assert_called_once_with(' topicwithspacefirst',1234567)

def test_topic_contains_space_last():
    # Setup
    t = transportMock()
    c = Pytelemetry(t)
    cb = mock.Mock(spec=["topic","data"])
    c.subscribe('topicwithspacefirst ',cb)

    c.publish('topicwithspacefirst ',1234567,'int32')
    assert t.queue.qsize() > 0
    c.update()
    assert t.queue.qsize() == 0
    cb.assert_called_once_with('topicwithspacefirst ',1234567)

def test_topic_contains_space_both_ends():
    # Setup
    t = transportMock()
    c = Pytelemetry(t)
    cb = mock.Mock(spec=["topic","data"])
    c.subscribe(' topicwithspaces ',cb)

    c.publish(' topicwithspaces ',1234567,'int32')
    assert t.queue.qsize() > 0
    c.update()
    assert t.queue.qsize() == 0
    cb.assert_called_once_with(' topicwithspaces ',1234567)

def test_end_to_end_uints():
    # Setup
    t = transportMock()
    c = Pytelemetry(t)
    cb = mock.Mock(spec=["topic","data"])
    default_cb = mock.Mock(spec=["topic","data"])
    c.subscribe('sometopic',cb)
    c.subscribe(None,default_cb)

    # testing callback subscribed to topic
    assert t.queue.qsize() == 0
    c.publish('sometopic',255,'uint8')
    assert t.queue.qsize() > 0
    c.update()
    assert t.queue.qsize() == 0
    cb.assert_called_with('sometopic',255)

    # testing callback subscribed to topic
    assert t.queue.qsize() == 0
    c.publish('sometopic',65535,'uint16')
    assert t.queue.qsize() > 0
    c.update()
    assert t.queue.qsize() == 0
    cb.assert_called_with('sometopic',65535)

    # testing callback subscribed to topic
    assert t.queue.qsize() == 0
    c.publish('sometopic',4294967295,'uint32')
    assert t.queue.qsize() > 0
    c.update()
    assert t.queue.qsize() == 0
    cb.assert_called_with('sometopic',4294967295)

def test_end_to_end_ints():
    # Setup
    t = transportMock()
    c = Pytelemetry(t)
    cb = mock.Mock(spec=["topic","data"])
    default_cb = mock.Mock(spec=["topic","data"])
    c.subscribe('sometopic',cb)
    c.subscribe(None,default_cb)

    # testing callback subscribed to topic
    assert t.queue.qsize() == 0
    c.publish('sometopic',127,'int8')
    assert t.queue.qsize() > 0
    c.update()
    assert t.queue.qsize() == 0
    cb.assert_called_with('sometopic',127)

    # testing callback subscribed to topic
    assert t.queue.qsize() == 0
    c.publish('sometopic',-127,'int8')
    assert t.queue.qsize() > 0
    c.update()
    assert t.queue.qsize() == 0
    cb.assert_called_with('sometopic',-127)

    # testing callback subscribed to topic
    assert t.queue.qsize() == 0
    c.publish('sometopic',32767,'int16')
    assert t.queue.qsize() > 0
    c.update()
    assert t.queue.qsize() == 0
    cb.assert_called_with('sometopic',32767)

    # testing callback subscribed to topic
    assert t.queue.qsize() == 0
    c.publish('sometopic',-32767,'int16')
    assert t.queue.qsize() > 0
    c.update()
    assert t.queue.qsize() == 0
    cb.assert_called_with('sometopic',-32767)

    # testing callback subscribed to topic
    assert t.queue.qsize() == 0
    c.publish('sometopic',2147483647,'int32')
    assert t.queue.qsize() > 0
    c.update()
    assert t.queue.qsize() == 0
    cb.assert_called_with('sometopic',2147483647)

    # testing callback subscribed to topic
    assert t.queue.qsize() == 0
    c.publish('sometopic',-2147483647,'int32')
    assert t.queue.qsize() > 0
    c.update()
    assert t.queue.qsize() == 0
    cb.assert_called_with('sometopic',-2147483647)

def test_end_to_end_floats():
    # Setup
    t = transportMock()
    c = Pytelemetry(t)
    cb = mock.Mock(spec=["topic","data"])
    default_cb = mock.Mock(spec=["topic","data"])
    c.subscribe('sometopic',cb)
    c.subscribe(None,default_cb)

    # testing callback subscribed to topic
    assert t.queue.qsize() == 0
    c.publish('sometopic',0.0,'float32')
    assert t.queue.qsize() > 0
    c.update()
    assert t.queue.qsize() == 0
    cb.assert_called_with('sometopic',0.0)

    # testing callback subscribed to topic
    assert t.queue.qsize() == 0
    c.publish('sometopic',3.4028234e38,'float32')
    assert t.queue.qsize() > 0
    c.update()
    assert t.queue.qsize() == 0
    assert abs(cb.call_args[0][1] - 3.4028234e38) <= max(1e-7 * max(abs(cb.call_args[0][1]), abs(3.4028234e38)), 0.0)

    # testing callback subscribed to topic
    assert t.queue.qsize() == 0
    c.publish('sometopic',-3.4028234e38,'float32')
    assert t.queue.qsize() > 0
    c.update()
    assert t.queue.qsize() == 0
    assert abs(cb.call_args[0][1] - (-3.4028234e38)) <= max(1e-7 * max(abs(cb.call_args[0][1]), abs(-3.4028234e38)), 0.0)
