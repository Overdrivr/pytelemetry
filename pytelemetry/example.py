import pytelemetry as tm
from transports.serialtransport import *
import time

def printer(topic, data):
    print(topic," : ", data)

transport = SerialTransport()
c = tm.pytelemetry(transport)

options = dict()
options['port'] = "COM20"
options['baudrate'] = 9600

transport.connect(options)
c.subscribe(None, printer)

c.publish('sometopic','booyaa','string')

timeout = time.time() + 3

while True:
    c.update()
    if time.time() > timeout:
        break

transport.disconnect()
print("Done.")
