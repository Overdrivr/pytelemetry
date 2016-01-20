import pytelemetry as tm
from transports.serialtransport import *

transportMock = SerialTransport()

c = tm.pytelemetry(transportMock)

c.publish(b'sometopic',b'booyaa','string')
