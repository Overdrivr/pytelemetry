[![PyPI version](https://badge.fury.io/py/pytelemetry.svg)](https://badge.fury.io/py/pytelemetry) [![Join the chat at https://gitter.im/Overdrivr/pytelemetry](https://badges.gitter.im/Overdrivr/pytelemetry.svg)](https://gitter.im/Overdrivr/pytelemetry?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge) [![Stories in Ready](https://badge.waffle.io/Overdrivr/pytelemetrycli.svg?label=ready&title=Ready)](http://waffle.io/Overdrivr/pytelemetrycli)
[![Build status](https://ci.appveyor.com/api/projects/status/03jtmphrld6k185v/branch/master?svg=true&passingText=master%20:%20OK&failingText=master%20:%20fail&pendingText=master%20:%20pending)](https://ci.appveyor.com/project/Overdrivr/pytelemetry/branch/master)
# pytelemetry

`pytelemetry` enables remote monitoring and control of embedded devices.
Specifically, `pytelemetry` implements a custom communication protocol, based on the [PubSub](https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern) (Publish/Subscribe) messaging pattern.

> [..] messages are published to "topics" or named logical channels. Subscribers in a topic-based system will receive all messages published to
> the topics to which they subscribe [..].
> *Source: Wikipedia*

This communication protocol is also available in a C library called [`telemetry`](https://github.com/Overdrivr/telemetry)
 that is specifically designed to run on all platforms and to be as light as possible.

![Overview](https://raw.githubusercontent.com/Overdrivr/pytelemetry/master/simple_overview.png)

Don't forget to check the [`bonus`](https://github.com/Overdrivr/pytelemetry#bonus) at the end.

## Usage
Data is published on `topics`. Topics can be seen as named communication channels.

First, instanciate one of the available transport class (*Note: so far, only serial transport is implemented*).
Then create a `Pytelemetry` object.

```python
from pytelemetry.pytelemetry import Pytelemetry
from pytelemetry.transports.serialtransport import SerialTransport
import time

# create a transport (Here based on pyserial)
transport = SerialTransport()
tlm = Pytelemetry(transport)

```

Connect the serial transport to serial port `COM20` at `9600` bauds.
```python

# connection options
options = dict()
options['port'] = "COM20"
options['baudrate'] = 9600

# connect
transport.connect(options)

```

Publish once to topic named `throttle`, sending effectively the value `0.8` of type `float` to the embedded device.

```python

# publish on a topic
tlm.publish('throttle',0.8,'float32')

```

Subscribe a `printer` function to all received topics.
Basically, this function will be called everytime a new frame is received.

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
Python 3.5 is supported. Support for python 3.4 and 3.3 will be added in a near future.

```bash
pip3 install pytelemetry
```

## Future improvements

In the next milestone, it is planned to make topics more meaningful (on the python-implementation only).
* Publishing to topics like `foo:2`, will add indexing data. This will add a nice support for arrays and sparse arrays.
* Publishing to topics like `bar\foo`, will add group data. This will indicate that there is a group called `bar`, with a subtopic called `foo`
* Combination : `bar\foobar\foo`,`bar\foobar\foo:2`
* Multiple instances : `bar\12\foo` will be understood as `foo` instance number 12 (useful if you want to have multiple instances under a same topic name)

For both python and C implementations of the protocol, it is also planned:
* add string compression with Huffman's Algorithm
* replace the byte stuffing algorithm by a consistent-over byte stuffing algorithm

 Both will contribute to reduce overhead and frames size.

## Bonus

You should also check the awesome command line interface [`pytelemetrycli`](https://github.com/Overdrivr/pytelemetrycli)[![PyPI version](https://badge.fury.io/py/pytelemetrycli.svg)](https://badge.fury.io/py/pytelemetrycli)

It makes communicating and debugging your embedded application effortless. With a few commands, it is possible to open high-performance graphs and plot your data in real time, list all available data channels, print samples of channel and much more.
