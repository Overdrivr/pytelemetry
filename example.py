from pytelemetry import Pytelemetry
from pytelemetry.transports.serialtransport import *
import time
import logging
from logging import getLogger
from logging import FileHandler
import datetime

def printer(topic, data, opts):
    print(topic," : ", data)

def init_logging():
    # Disable default stderr handler
    root = getLogger().addHandler(logging.NullHandler())

    # Get the loggers used in pytelemetry.telemetry.telemetry file
    rx = getLogger("telemetry.rx")
    tx = getLogger("telemetry.tx")
    rx.setLevel(logging.DEBUG)
    tx.setLevel(logging.DEBUG)

    # Format how data will be .. formatted
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

    # Create a handler to save logging output to a file
    dateTag = datetime.datetime.now().strftime("%Y-%b-%d_%H-%M-%S")
    in_handler = FileHandler('in-%s.log' % dateTag)
    in_handler.setLevel(logging.DEBUG) # Also pass all messages
    in_handler.setFormatter(formatter)

    out_handler = FileHandler('out-%s.log' % dateTag)
    out_handler.setLevel(logging.DEBUG) # Also pass all messages
    out_handler.setFormatter(formatter)

    # Attach the logger to the handler
    rx.addHandler(in_handler)
    tx.addHandler(out_handler)


def main():
    init_logging()

    transport = SerialTransport()
    c = Pytelemetry(transport)

    options = dict()
    options['port'] = "COM20"
    options['baudrate'] = 115200

    transport.connect(options)
    #c.subscribe(None, printer)

    bad_frame = bytearray(b'0700736f6d65746f70696300626f6f7961613ecc')
    c.api._decode_frame(bad_frame)

    c.publish('sometopic','booyaa','string')

    timeout = time.time() + 3

    while True:
        c.update()
        if time.time() > timeout:
            break

    transport.disconnect()
    print("Done.")

if __name__ == "__main__":
    main()
