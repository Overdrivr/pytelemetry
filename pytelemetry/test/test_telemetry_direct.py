from pytelemetry.telemetry.telemetry import Telemetry

def test_special_characters():
    t = Telemetry(None,None)

    tests = [ ('foo', 'bar é$à', 'string'),
              ('çé', 2**30, 'int32'),
              ('yolo', 32768, 'uint16') ]

    for topic, data, typ in tests:
        frame = bytes(t._encode_frame(topic, data, typ))
        decoded = t._decode_frame(frame)
        assert decoded == (topic, data), '%s != %s' % (decoded, (topic, data))
