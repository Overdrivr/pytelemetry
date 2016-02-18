from .crc import crc16
from .framing import Delimiter
from struct import pack, unpack, unpack_from

class Telemetry:
    """
Low level telemetry protocol (github.com/Overdrivr/Telemetry) implemented in python
    """
    def __init__(self, transport, callback):
        self.transport = transport
        self.on_frame_callback = callback
        self.delimiter = Delimiter(self._on_frame_detected)
        self.types = {'float32' : 0,
                      'uint8'   : 1,
                      'uint16'  : 2,
                      'uint32'  : 3,
                      'int8'    : 4,
                      'int16'   : 5,
                      'int32'   : 6,
                      'string'  : 7}

        self.sizes = {'float32' : 4,
                      'uint8'   : 1,
                      'uint16'  : 2,
                      'uint32'  : 4,
                      'int8'    : 1,
                      'int16'   : 2,
                      'int32'   : 4}

        self.rtypes = dict(zip(self.types.values(), self.types.keys()))

        self.formats = {'float32' : "f",
                        'uint8'   : "B",
                        'uint16'  : "H",
                        'uint32'  : "L",
                        'int8'    : "b",
                        'int16'   : "h",
                        'int32'   : "l"}

    def publish(self, topic, data, datatype):
        # header
        if not datatype in self.types:
            return # Not raising exceptions for now for consistency with C API
            # TODO: To fix
            #raise IndexError("Provided datatype ",datatype," unknown.")

        topic = topic.encode('utf8')

        if datatype == "string":
            data = data.encode("utf8")
            payload_fmt = "%ds" % len(data)
        else:
            payload_fmt = self.formats[datatype]

        frame = pack("<H%dsB%s" % (len(topic), payload_fmt), 
                        self.types[datatype], 
                        topic, 0, 
                        data)
        frame = bytearray(frame)

        # crc
        _crc = crc16(frame)
        _crc = pack("<H",_crc)
        frame.extend(_crc)

        # bytestuff
        frame = self.delimiter.encode(frame)

        # send
        if self.transport.writeable():
            self.transport.write(frame)

    def update(self):
        amount = self.transport.readable();
        for i in range(amount):
            c = self.transport.read(maxbytes=1)
            self.delimiter.decode(c)

    def _on_frame_detected(self, frame):
        if len(frame) < 2:
            return
        #import pdb; pdb.set_trace()
        # check crc
        local_crc = crc16(frame[:-2])
        frame_crc, = unpack("<H", frame[-2:])
        if local_crc != frame_crc:
            return

        # header
        header, = unpack_from("<H", frame)
        if not header in self.rtypes:
            return

        # locate EOL
        try:
            i = frame.index(0, 2, -2)
        except:
            return

        # decode topic
        topic = frame[2:i].decode("utf8")

        # Find type from header
        _type = self.rtypes[header]
        # decode data
        if _type == "string":
            # start at i+1 to remove EOL zero
            data = frame[i+1:-2].decode("utf8")
        else:
            # Find format
            fmt = self.formats[_type]
            # Check actual sizes matches the one expected by unpack
            # (start at i+1 to remove EOL zero)
            if len(frame[i+1:-2]) != self.sizes[_type]:
                return
            data, = unpack_from(fmt, frame, i+1)

        self.on_frame_callback(topic, data)


if __name__ == '__main__':
    t = Telemetry(None,None)

    t.publish('sometopic ',12457,"int32")
