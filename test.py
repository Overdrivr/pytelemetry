import pytelemetry as tm

transportMock = None

c = tm.pytelemetry(transportMock)

c.publish(b'sometopic',b'booyaa','string')
