from .. import crc
from .. import framing

class Telemetry:
    """
    Low level telemetry protocol (github.com/Overdrivr/Telemetry)
    """
    def __init__(self,transport, on_frame_callback):
        self.transport = transport
        self.on_frame_callback = on_frame_callback
        self.types = ['string','uint8','uint16','uint32','int8','int16','int32','float32']

    def publish(self,topic, data, datatype):
        pass

    def update(self):
        pass

    def _emplace(msg,data):
        pass
