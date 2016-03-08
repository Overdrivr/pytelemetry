from pytelemetry import Pytelemetry
import queue
import unittest.mock as mock
from pytelemetry.telemetry.crc import crc16
import struct

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
    cb = mock.Mock(spec=["topic","data","opts"])
    default_cb = mock.Mock(spec=["topic","data","opts"])
    c.subscribe('sometopic',cb)
    c.subscribe(None,default_cb)

    # testing callback subscribed to topic
    assert t.queue.qsize() == 0
    c.publish('sometopic','someMessage','string')
    assert t.queue.qsize() > 0
    c.update()
    assert t.queue.qsize() == 0
    cb.assert_called_once_with('sometopic','someMessage',None)

    # test default callback
    c.publish('othertopic','otherMessage','string')
    assert t.queue.qsize() > 0
    c.update()
    assert t.queue.qsize() == 0
    default_cb.assert_called_once_with('othertopic','otherMessage',None)

def test_topic_contains_space_first():
    # Setup
    t = transportMock()
    c = Pytelemetry(t)
    cb = mock.Mock(spec=["topic","data","opts"])
    c.subscribe(' topicwithspacefirst',cb)

    c.publish(' topicwithspacefirst',1234567,'int32')
    assert t.queue.qsize() > 0
    c.update()
    assert t.queue.qsize() == 0
    cb.assert_called_once_with(' topicwithspacefirst',1234567,None)

def test_topic_contains_space_last():
    # Setup
    t = transportMock()
    c = Pytelemetry(t)
    cb = mock.Mock(spec=["topic","data","opts"])
    c.subscribe('topicwithspacefirst ',cb)

    c.publish('topicwithspacefirst ',1234567,'int32')
    assert t.queue.qsize() > 0
    c.update()
    assert t.queue.qsize() == 0
    cb.assert_called_once_with('topicwithspacefirst ',1234567,None)

def test_topic_contains_space_both_ends():
    # Setup
    t = transportMock()
    c = Pytelemetry(t)
    cb = mock.Mock(spec=["topic","data","opts"])
    c.subscribe(' topicwithspaces ',cb)

    c.publish(' topicwithspaces ',1234567,'int32')
    assert t.queue.qsize() > 0
    c.update()
    assert t.queue.qsize() == 0
    cb.assert_called_once_with(' topicwithspaces ',1234567,None)

def test_end_to_end_uints():
    # Setup
    t = transportMock()
    c = Pytelemetry(t)
    cb = mock.Mock(spec=["topic","data","opts"])
    default_cb = mock.Mock(spec=["topic","data","opts"])
    c.subscribe('sometopic',cb)
    c.subscribe(None,default_cb)

    # testing callback subscribed to topic
    assert t.queue.qsize() == 0
    c.publish('sometopic',255,'uint8')
    assert t.queue.qsize() > 0
    c.update()
    assert t.queue.qsize() == 0
    cb.assert_called_with('sometopic',255,None)

    # testing callback subscribed to topic
    assert t.queue.qsize() == 0
    c.publish('sometopic',65535,'uint16')
    assert t.queue.qsize() > 0
    c.update()
    assert t.queue.qsize() == 0
    cb.assert_called_with('sometopic',65535,None)

    # testing callback subscribed to topic
    assert t.queue.qsize() == 0
    c.publish('sometopic',4294967295,'uint32')
    assert t.queue.qsize() > 0
    c.update()
    assert t.queue.qsize() == 0
    cb.assert_called_with('sometopic',4294967295,None)

def test_end_to_end_ints():
    # Setup
    t = transportMock()
    c = Pytelemetry(t)
    cb = mock.Mock(spec=["topic","data","opts"])
    default_cb = mock.Mock(spec=["topic","data","opts"])
    c.subscribe('sometopic',cb)
    c.subscribe(None,default_cb)

    # testing callback subscribed to topic
    assert t.queue.qsize() == 0
    c.publish('sometopic',127,'int8')
    assert t.queue.qsize() > 0
    c.update()
    assert t.queue.qsize() == 0
    cb.assert_called_with('sometopic',127,None)

    # testing callback subscribed to topic
    assert t.queue.qsize() == 0
    c.publish('sometopic',-127,'int8')
    assert t.queue.qsize() > 0
    c.update()
    assert t.queue.qsize() == 0
    cb.assert_called_with('sometopic',-127,None)

    # testing callback subscribed to topic
    assert t.queue.qsize() == 0
    c.publish('sometopic',32767,'int16')
    assert t.queue.qsize() > 0
    c.update()
    assert t.queue.qsize() == 0
    cb.assert_called_with('sometopic',32767,None)

    # testing callback subscribed to topic
    assert t.queue.qsize() == 0
    c.publish('sometopic',-32767,'int16')
    assert t.queue.qsize() > 0
    c.update()
    assert t.queue.qsize() == 0
    cb.assert_called_with('sometopic',-32767,None)

    # testing callback subscribed to topic
    assert t.queue.qsize() == 0
    c.publish('sometopic',2147483647,'int32')
    assert t.queue.qsize() > 0
    c.update()
    assert t.queue.qsize() == 0
    cb.assert_called_with('sometopic',2147483647,None)

    # testing callback subscribed to topic
    assert t.queue.qsize() == 0
    c.publish('sometopic',-2147483647,'int32')
    assert t.queue.qsize() > 0
    c.update()
    assert t.queue.qsize() == 0
    cb.assert_called_with('sometopic',-2147483647,None)

def test_end_to_end_floats():
    # Setup
    t = transportMock()
    c = Pytelemetry(t)
    cb = mock.Mock(spec=["topic","data","opts"])
    default_cb = mock.Mock(spec=["topic","data","opts"])
    c.subscribe('sometopic',cb)
    c.subscribe(None,default_cb)

    # testing callback subscribed to topic
    assert t.queue.qsize() == 0
    c.publish('sometopic',0.0,'float32')
    assert t.queue.qsize() > 0
    c.update()
    assert t.queue.qsize() == 0
    cb.assert_called_with('sometopic',0.0,None)

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


def test_protocol_stats():
    t = transportMock()
    p = Pytelemetry(t)

    measures = p.api.stats()

    assert measures["rx_decoded_frames"] == 0
    assert measures["rx_corrupted_crc"] == 0
    assert measures["rx_corrupted_header"] == 0
    assert measures["rx_corrupted_eol"] == 0
    assert measures["rx_corrupted_topic"] == 0
    assert measures["rx_corrupted_payload"] == 0
    assert measures["tx_encoded_frames"] == 0

    # Add a frame inside the transport queue
    t.write(bytearray.fromhex("f70700666f6f0062617247027f"))
    # update to read the new frame
    p.update()
    # get measurements
    measures = p.api.stats()

    assert measures["rx_decoded_frames"] == 1
    assert measures["rx_corrupted_crc"] == 0
    assert measures["rx_corrupted_header"] == 0
    assert measures["rx_corrupted_eol"] == 0
    assert measures["rx_corrupted_topic"] == 0
    assert measures["rx_corrupted_payload"] == 0
    assert measures["tx_encoded_frames"] == 0

    # replaced CRC '4702' by '4701' to corrupt crc
    t.write(bytearray.fromhex("f70700666f6f0062617247017f"))
    # update to read the new frame
    p.update()
    # get measurements
    measures = p.api.stats()

    assert measures["rx_decoded_frames"] == 1
    assert measures["rx_corrupted_crc"] == 1
    assert measures["rx_corrupted_header"] == 0
    assert measures["rx_corrupted_eol"] == 0
    assert measures["rx_corrupted_topic"] == 0
    assert measures["rx_corrupted_payload"] == 0
    assert measures["tx_encoded_frames"] == 0

    # replaced byte n3 '00' by '10' to corrupt crc
    t.write(bytearray.fromhex("f70710666f6f0062617247027f"))
    # update to read the new frame
    p.update()
    # get measurements
    measures = p.api.stats()

    assert measures["rx_decoded_frames"] == 1
    assert measures["rx_corrupted_crc"] == 2
    assert measures["rx_corrupted_header"] == 0
    assert measures["rx_corrupted_eol"] == 0
    assert measures["rx_corrupted_topic"] == 0
    assert measures["rx_corrupted_payload"] == 0
    assert measures["tx_encoded_frames"] == 0

    #crc = crc16(bytearray.fromhex("0900666f6f00626172"))
    #print(crc)
    #crc = struct.pack("<H",crc)
    #print(crc.hex())

    # Replaced header from 0700 to 0900 to corrupt it. Crc is valid to not discard
    t.write(bytearray.fromhex("f70900666f6f006261725fc57f"))
    # update to read the new frame
    p.update()
    # get measurements
    measures = p.api.stats()

    assert measures["rx_decoded_frames"] == 1
    assert measures["rx_corrupted_crc"] == 2
    assert measures["rx_corrupted_header"] == 1
    assert measures["rx_corrupted_eol"] == 0
    assert measures["rx_corrupted_topic"] == 0
    assert measures["rx_corrupted_payload"] == 0
    assert measures["tx_encoded_frames"] == 0

    #crc = crc16(bytearray.fromhex("0700666f6f01626172"))
    #print(crc)
    #crc = struct.pack("<H",crc)
    #print(crc.hex())

    # Removed EOL. Crc is valid to not discard
    t.write(bytearray.fromhex("f70700666f6f0162617224417f"))
    # update to read the new frame
    p.update()
    # get measurements
    measures = p.api.stats()

    assert measures["rx_decoded_frames"] == 1
    assert measures["rx_corrupted_crc"] == 2
    assert measures["rx_corrupted_header"] == 1
    assert measures["rx_corrupted_eol"] == 1
    assert measures["rx_corrupted_topic"] == 0
    assert measures["rx_corrupted_payload"] == 0
    assert measures["tx_encoded_frames"] == 0

    # Impossible to detect corrupted payload of type string because length is unkown. One more reason to store framesize inside frame

    # Use a frame of type u32 instead
    #crc = crc16(bytearray.fromhex("03006b6c6d6f707100ffffff"))
    #crc = struct.pack("<H",crc)
    #print(crc.hex())

    # Corruped payload by removing third & fourth hex number from end. Crc will pass
    #
    t.write(bytearray.fromhex("f703006b6c6d6f707100fffffff2dd7f"))
    # update to read the new frame
    p.update()
    # get measurements
    measures = p.api.stats()

    assert measures["rx_decoded_frames"] == 1
    assert measures["rx_corrupted_crc"] == 2
    assert measures["rx_corrupted_header"] == 1
    assert measures["rx_corrupted_eol"] == 1
    assert measures["rx_corrupted_topic"] == 0
    assert measures["rx_corrupted_payload"] == 1
    assert measures["tx_encoded_frames"] == 0

    topmeasures = p.stats()

    assert measures["rx_decoded_frames"] == topmeasures['protocol']["rx_decoded_frames"]
    assert measures["rx_corrupted_crc"] == topmeasures['protocol']["rx_corrupted_crc"]
    assert measures["rx_corrupted_header"] == topmeasures['protocol']["rx_corrupted_header"]
    assert measures["rx_corrupted_eol"] == topmeasures['protocol']["rx_corrupted_eol"]
    assert measures["rx_corrupted_topic"] == topmeasures['protocol']["rx_corrupted_topic"]
    assert measures["rx_corrupted_payload"] == topmeasures['protocol']["rx_corrupted_payload"]
    assert measures["tx_encoded_frames"] == topmeasures['protocol']["tx_encoded_frames"]

    p.publish("boo", 123, "uint8")

    # get measurements
    measures = p.stats()

    assert measures['protocol']["rx_decoded_frames"] == 1
    assert measures['protocol']["rx_corrupted_crc"] == 2
    assert measures['protocol']["rx_corrupted_header"] == 1
    assert measures['protocol']["rx_corrupted_eol"] == 1
    assert measures['protocol']["rx_corrupted_topic"] == 0
    assert measures['protocol']["rx_corrupted_payload"] == 1
    assert measures['protocol']["tx_encoded_frames"] == 1

    measures = p.api.delimiter.stats()

    assert measures["rx_processed_bytes"] > 0
    assert measures["rx_discarded_bytes"] == 0
    assert measures["rx_escaped_bytes"] == 0
    assert measures["rx_complete_frames"] > 0
    assert measures["rx_uncomplete_frames"] == 0
    assert measures["tx_processed_bytes"] > 0
    assert measures["tx_encoded_frames"] > 0
    assert measures["tx_escaped_bytes"] == 0

    p.resetStats()
    measures = p.stats()

    assert measures['protocol']["rx_decoded_frames"] == 0
    assert measures['protocol']["rx_corrupted_crc"] == 0
    assert measures['protocol']["rx_corrupted_header"] == 0
    assert measures['protocol']["rx_corrupted_eol"] == 0
    assert measures['protocol']["rx_corrupted_topic"] == 0
    assert measures['protocol']["rx_corrupted_payload"] == 0
    assert measures['protocol']["tx_encoded_frames"] == 0

    assert measures['framing']["rx_processed_bytes"] == 0
    assert measures['framing']["rx_discarded_bytes"] == 0
    assert measures['framing']["rx_escaped_bytes"] == 0
    assert measures['framing']["rx_complete_frames"] == 0
    assert measures['framing']["rx_uncomplete_frames"] == 0
    assert measures['framing']["tx_processed_bytes"] == 0
    assert measures['framing']["tx_encoded_frames"] == 0
    assert measures['framing']["tx_escaped_bytes"] == 0
