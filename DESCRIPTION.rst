pytelemetry
==========

Overview
========
This module implements a powerful communication protocol that makes
remote control and monitoring  of embedded devices an effortless task.


```python
from pytelemetry import Pytelemetry
from pytelemetry.transports.serialtransport import SerialTransport
import time

transport = SerialTransport()
tlm = Pytelemetry(transport)
transport.connect({port:'com9',baudrate:'9600'})

# publish on a topic (a named communication channel)
tlm.publish('throttle',0.8,'float32')

def printer(topic, data, opts):
    print(topic," : ", data)

#Subscribe a `printer` function called on every frame with topic 'feedback'.
tlm.subscribe("feedback", printer)

# Update during 3 seconds
timeout = time.time() + 3
while True:
    tlm.update()
    if time.time() > timeout:
        break

# disconnect
transport.disconnect()
print("Done.")
```

Language C implementation
=========================
Telemetry is the same protocol implemented in C.
- Project page: https://github.com/Overdrivr/Telemetry

Command Line Interface (CLI)
============================
Pytelemetry CLI is a powerful command interface perfectly suited for fast
 prototyping with this protocol.
It allows opening plots on embedded data on-the-fly, publishing data on any
topics, listing serial port and much more.

- Project page: https://github.com/Overdrivr/pytelemetrycli


Centralized documentation
=========================
The documentation for all three projects is available here: https://github.com/Overdrivr/Telemetry/wiki

MIT License, (C) 2015-2016 Rémi Bèges <remi.beges@gmail.com>
