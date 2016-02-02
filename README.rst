# pytelemetry
pytelemetry enables remote monitoring and control of embedded devices.
It is a python wrapper of the (telemetry C library)[https://github.com/Overdrivr/Telemetry]

## Usage
```python
import pytelemetry.pytelemetry as tm
from pytelemetry.transports.serialtransport import *
import time

def printer(topic, data):
    print(topic," : ", data)

# create a transport (Here based on pyserial)
transport = SerialTransport()
# create the pytelemetry object
c = tm.pytelemetry(transport)

# connection options
options = dict()
options['port'] = "COM20"
options['baudrate'] = 9600

# connect
transport.connect(options)

# subscribe to a topic. Subscribing to None subscribes to all
c.subscribe(None, printer)

# publish on a topic
c.publish('throttle',0.8,'float32')

# Update during 3 seconds
timeout = time.time() + 3
while True:
    c.update()
    if time.time() > timeout:
        break

# disconnect
transport.disconnect()
```
The library relies on a Publishing/Subscribing mechanism. Publishing on one side triggers a call to 
### publish

### subscribe

## Installation
Python 3.5+ only is supported.
### Windows
```bash
pip install pytelemetry
```

### Unix
*Note : This workflow has not been tested yet because I don't work under Unix. Feel free to test it and bring some feedback.*

On Unix, you need to recompile the C API because python binary distributions (wheels) are not yet supported.
This can be done with a few commands. The build system will look for a GCC compatible toolchain.

```bash
gradlew cloneGitRepo
gradlew :c:Telemetry:build
gradlew copyFiles
```
Then you can build the python package and install it with pip from the local files.
Place your terminal on the pytelemetry repository **root** project (`./pytelemetry`, not `./pytelemetry/pytelemetry`)
```bash
python setup.py bdist_wheel
pip install -e .
```

### Mac OS
*Note : No precompiled binaries available yet. You need to compile from source just like Unix.*
'''bash
pip install pytelemetry
```
