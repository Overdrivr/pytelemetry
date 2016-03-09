[![PyPI version](https://badge.fury.io/py/pytelemetry.svg)](https://badge.fury.io/py/pytelemetry) [![Join the chat at https://gitter.im/Overdrivr/pytelemetry](https://badges.gitter.im/Overdrivr/pytelemetry.svg)](https://gitter.im/Overdrivr/pytelemetry?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge) [![Stories in Ready](https://badge.waffle.io/Overdrivr/pytelemetrycli.svg?label=ready&title=Ready)](http://waffle.io/Overdrivr/pytelemetrycli)
*Windows* [![Build status](https://ci.appveyor.com/api/projects/status/03jtmphrld6k185v/branch/master?svg=true&passingText=master%20:%20OK&failingText=master%20:%20fail&pendingText=master%20:%20pending)](https://ci.appveyor.com/project/Overdrivr/pytelemetry/branch/master)
*Linux* [![Build Status](https://travis-ci.org/Overdrivr/pytelemetry.svg?branch=master)](https://travis-ci.org/Overdrivr/pytelemetry)
# pytelemetry

![Overview](https://raw.githubusercontent.com/Overdrivr/Telemetry/master/pubsub_overview.png)

* `pytelemetry` provides high-level communication with any embedded device for
remote control and monitoring.
Specifically, `pytelemetry` implements a custom communication protocol, based on
the [PubSub](https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern)
(Publish/Subscribe) messaging pattern.

* [`telemetry`](https://github.com/Overdrivr/telemetry) is the C implementation
of the protocol. It can run on any embedded system, along with official
distributions for Arduino and ARM Mbed.

* [`pytelemetrycli`](https://github.com/Overdrivr/pytelemetrycli)
[![PyPI version](https://badge.fury.io/py/pytelemetrycli.svg)](https://badge.fury.io/py/pytelemetrycli)
is a powerful command line interface to interact with
embedded devices using the protocol. It enables instant **data visualization**
of any received data, **full logging** of communications, **health monitoring**
of the serial port and much more.


## Usage
Data is exchanged on named communication channels called `topics`.

First, instanciate one of the available transport class (*Note: so far, only serial transport is implemented*) and the `Pytelemetry` object.

```python
from pytelemetry import Pytelemetry
from pytelemetry.transports.serialtransport import SerialTransport
import time

# create a transport (Here based on pyserial) to exchange data through serial port
transport = SerialTransport()

# Top level Pytelemetry api
tlm = Pytelemetry(transport)

# Connection to serial port `COM20` at `9600` bauds.
transport.connect({'port': "com20", 'baudrate': 9600})

```

Publish once to topic named `throttle`, sending effectively the value `0.8` of type `float` to the embedded device.

```python

# publish on a topic
tlm.publish('throttle',0.8,'float32')

```

Subscribe a `printer` function to all received topics.
Basically, this function will be called every time a new frame is received.

``` python
def printer(topic, data):
    print(topic," : ", data)

# subscribe to a topic. Subscribing to None subscribes to all
tlm.subscribe(None, printer)
```

Then, run an update during 3 seconds and disconnect after.

```python
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
If the embedded device published regularly on topic `foo` with an incrementing value, you should see in the console:

```bash
foo : 34
foo : 35
foo : 36
foo : 37
Done.
```

## Installation
Python 3.3 and upward is supported. Python 2.x is not supported for now.

```bash
pip3 install pytelemetry
```

# Advanced features

* Support for arrays and sparse arrays. Send individual array items along with their item using topics like `foo:2`. '2' is used here for the index, the value is provided inside the payload.

## Future improvements

In the next milestone, it is planned to make topics more meaningful (on the python-implementation only).

* Publishing to topics like `bar\foo`, will add group data. This will indicate that there is a group called `bar`, with a subtopic called `foo`
* Combination : `bar\foobar\foo`,`bar\foobar\foo:2`
* Multiple instances : `bar\12\foo` will be understood as `foo` instance number 12 (useful if you want to have multiple instances under a same topic name)

For both python and C implementations of the protocol, it is also planned:
* add string compression with Huffman's Algorithm
* replace the byte stuffing algorithm by a consistent-over byte stuffing algorithm

 Both will contribute to reduce overhead and frames size.
