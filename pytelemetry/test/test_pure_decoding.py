import pytest
from pytelemetry.telemetry.telemetry import Telemetry
from pytelemetry.telemetry.framing import Delimiter

class Cache:
    frame = []

def cb(data):
    Cache.frame = data
    print(data)

def test_reference_vector():
    t = Telemetry(None,None)
    d = Delimiter(cb)

    d.decode(bytearray.fromhex("f70700666f6f0062617247027f"))
    assert t._decode_frame(Cache.frame) == ('foo','bar')

    d.decode(bytearray.fromhex("f70700666f6f2077697468207370616365730062617220776974682073706163657317dc7f"))
    assert t._decode_frame(Cache.frame) == ('foo with spaces','bar with spaces')

    d.decode(bytearray.fromhex("f7070030313233343536373839003031323334353637383973c07f"))
    assert t._decode_frame(Cache.frame) == ('0123456789', '0123456789')


    d.decode(bytearray.fromhex("f703006b6c6d6f707100ffffffff107b7f"))
    assert t._decode_frame(Cache.frame) == ('klmopq', 4294967295)


def test_some_frames():
    t = Telemetry(None,None)
    assert t._decode_frame(bytearray.fromhex("0100626f7574746f6e300000b92c")) == ('boutton0',0)
    assert t._decode_frame(bytearray.fromhex("0100626f7574746f6e3100005f2a")) == ('boutton1',0)
    assert t._decode_frame(bytearray.fromhex("0300636d70740029000000e867")) == ('cmpt', 41)
    assert t._decode_frame(bytearray.fromhex("0300636d70740006000000d269")) == ('cmpt', 6)
    assert t._decode_frame(bytearray(b"\x03\x00cmpt\x00\xc7\x00\x00\x00\x83e")) == ('cmpt', 199)


def test_delimiter_stats():
    t = Telemetry(None,None)
    d = Delimiter(cb)

    measures = d.stats()

    assert measures["rx_processed_bytes"] == 0
    assert measures["rx_discarded_bytes"] == 0
    assert measures["rx_escaped_bytes"] == 0
    assert measures["rx_complete_frames"] == 0
    assert measures["rx_uncomplete_frames"] == 0
    assert measures["tx_processed_bytes"] == 0
    assert measures["tx_encoded_frames"] == 0
    assert measures["tx_escaped_bytes"] == 0

    d.decode(bytearray.fromhex("f70700666f6f0062617247027f"))

    measures = d.stats()

    assert measures["rx_processed_bytes"] == 13
    assert measures["rx_discarded_bytes"] == 0
    assert measures["rx_escaped_bytes"] == 0
    assert measures["rx_complete_frames"] == 1
    assert measures["rx_uncomplete_frames"] == 0
    assert measures["tx_processed_bytes"] == 0
    assert measures["tx_encoded_frames"] == 0
    assert measures["tx_escaped_bytes"] == 0

    # Added 'eade' to previous frame
    d.decode(bytearray.fromhex("eadef70700666f6f0062617247027f"))

    measures = d.stats()

    assert measures["rx_processed_bytes"] == 13 + 13 + 2
    assert measures["rx_discarded_bytes"] == 2
    assert measures["rx_escaped_bytes"] == 0
    assert measures["rx_complete_frames"] == 2
    assert measures["rx_uncomplete_frames"] == 0
    assert measures["tx_processed_bytes"] == 0
    assert measures["tx_encoded_frames"] == 0
    assert measures["tx_escaped_bytes"] == 0

    # Added 'f7eade' to original frame
    d.decode(bytearray.fromhex("f7eadef70700666f6f0062617247027f"))

    measures = d.stats()

    assert measures["rx_processed_bytes"] == 13 + 13 + 2 + 13 + 3
    assert measures["rx_discarded_bytes"] == 2 # bytes eade after f7 are not discarded because after a valid SOF
    assert measures["rx_escaped_bytes"] == 0
    assert measures["rx_complete_frames"] == 3
    assert measures["rx_uncomplete_frames"] == 1 # but 1 more uncomplete frame
    assert measures["tx_processed_bytes"] == 0
    assert measures["tx_encoded_frames"] == 0
    assert measures["tx_escaped_bytes"] == 0

    # Dummy frame to test escaping
    d.decode(bytearray.fromhex("f7007df7007d7d007d7f7f"))

    measures = d.stats()

    assert measures["rx_processed_bytes"] == 13 + 13 + 2 + 13 + 3 + 11
    assert measures["rx_discarded_bytes"] == 2
    assert measures["rx_escaped_bytes"] == 3 # 3 escaped bytes
    assert measures["rx_complete_frames"] == 4
    assert measures["rx_uncomplete_frames"] == 1
    assert measures["tx_processed_bytes"] == 0
    assert measures["tx_encoded_frames"] == 0
    assert measures["tx_escaped_bytes"] == 0
