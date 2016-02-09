from .crc import crc16
from .framing import Delimiter
from struct import pack, unpack, unpack_from

class Telemetry:
    """
Low level telemetry protocol (github.com/Overdrivr/Telemetry) implemented in python
    """
    def __init__(self,transport, on_frame_callback):
        self.transport = transport
        self.on_frame_callback = on_frame_callback
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

        self.rtypes = {0 : 'float32',
                       1 : 'uint8',
                       2 : 'uint16',
                       3 : 'uint32',
                       4 : 'int8',
                       5 : 'int16',
                       6 : 'int32',
                       7 : 'string'}

        self.formats = {'float32' : ">f",
                        'uint8'   : ">B",
                        'uint16'  : ">H",
                        'uint32'  : ">L",
                        'int8'    : ">b",
                        'int16'   : ">h",
                        'int32'   : ">l"}

    def publish(self,topic, data, datatype):
        frame = bytearray()

        # header
        if not datatype in self.types:
            raise IndexError("Provided datatype ",datatype," unknown.")

        header = pack(">H",self.types[datatype])
        for b in header:
            frame.append(b)

        # topic
        for b in topic.encode('ASCII'):
            frame.append(b)
        # EOL
        frame.append(0)

        # payload
        payload = None

        if datatype == "string":
            payload = data.encode("ASCII")
        else:
            payload = pack(self.formats[datatype],data)

        for b in payload:
            frame.append(b)

        # crc
        _crc = crc16(frame)
        _crc = pack(">H",_crc)

        for b in _crc:
            frame.append(b)

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

        # check crc
        local_crc = crc16(frame[:-2])
        frame_crc, = unpack_from(">H", frame[-2:], offset=0)

        if local_crc != frame_crc:
            return

        # header
        header, = unpack_from(">H", frame, offset=0)

        # locate EOL
        try:
            i = frame[2:-2].find(0) + 2 # Account for offset of 2 induced by sciling
        except:
            return

        # decode topic
        topic = frame[2:i].decode(encoding="utf-8")

        if not header in self.rtypes:
            return

        # Find type from header
        _type = self.rtypes[header]

        # decode data
        if _type == "string":
            # start at i+1 to remove EOL zero
            data = frame[i+1:-2].decode(encoding="utf-8")
        else:
            # Find format
            fmt = self.formats[_type]
            # Check actual sizes matches the one expected by unpack
            if len(frame[i:-2]) != self.sizes[_type]:
                return
            data = unpack(fmt,frame[i:-2])
        
        self.on_frame_callback(topic, data)


if __name__ == '__main__':
    t = Telemetry(None,None)

    t.publish("test",235,"float32")
