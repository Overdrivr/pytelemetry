from .crc import crc16
from .framing import Delimiter
from struct import pack

class Telemetry:
    """
    Low level telemetry protocol (github.com/Overdrivr/Telemetry)
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
        pass

    def _emplace(self, msg, data):
        pass

    def _on_frame_detected(self, payload):
        pass

if __name__ == '__main__':
    t = Telemetry(None,None)

    t.publish("test",235,"float32")
