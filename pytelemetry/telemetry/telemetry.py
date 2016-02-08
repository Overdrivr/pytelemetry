#from . import crc
#from . import framing

class Telemetry:
    """
    Low level telemetry protocol (github.com/Overdrivr/Telemetry)
    """
    def __init__(self,transport, on_frame_callback):
        self.transport = transport
        self.on_frame_callback = on_frame_callback

    def publish(topic, data, datatype):
        pass

    def subscribe(topic,callback):
        pass

    def update():
        pass

    def _emplace(msg,data):
        pass
