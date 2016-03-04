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
