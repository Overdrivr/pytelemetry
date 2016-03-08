from pytelemetry.telemetry.telemetry import Telemetry
from pytelemetry.telemetry.c_binding import TelemetryCBinding
from pytelemetry.remoting import translate

__all__ = ['Pytelemetry']

_telemetry_use_c_api = False

# pytelemetry interface
class Pytelemetry:
    """
        Main class for the pytelemetry library.

        If you intend to implement a new transport, it needs to implement these
        four methods:

        >>> read(bytesAmount)
        Expects: Amount of bytes to read. Will return less bytes if
        bytes amount is bigger than immediately available bytes amount
        Returns: A bytes instance containing read bytes

        >>> readable()
        Returns: Amount of immediately available bytes

        >>> write(data)
        Expects: a bytes instance containing the data to write
        Returns: True

        >>> writeable()
        Returns: True if transport is available for writing,
                 False otherwise

    """
    def __init__(self, transport):
        """
            Creates a new instance of the Pytelemetry class.

            :param transport: A transport-compliant class. See Pytelemetry class
            documentation for more information
        """

        self.callbacks = dict()
        self.default_callback = None

        if _telemetry_use_c_api:
            self.api = TelemetryCBinding(transport,self._on_frame)
        else:
            self.api = Telemetry(transport,self._on_frame)

    def resetStats(self):
        """
Resets all counters that monitor transport and protocol to 0.
        """
        self.api.delimiter.resetStats()
        self.api.resetStats()

    def stats(self):
        """
Returns a dictionnary of dictionnary that contains critical information
about the transport and protocol behavior, such as:
   * amount of received frames
   * amount of badly delimited frames
   * amount of correctly delimited but still corrupted frames
   * etc
        """
        d = dict()
        d['framing'] = self.api.delimiter.stats()
        d['protocol'] = self.api.stats()

        return d

    def publish(self, topic, data, datatype):
        """

        """
        self.api.publish(topic,data,datatype)

    # subscribe a callback to topic
    # Subscribing to None will call that function for any unsubscribed topic
    def subscribe(self, topic, cb):
        if topic:
            self.callbacks[topic] = cb
        else:
            self.default_callback = cb

    def update(self):
        self.api.update()

    def _on_frame(self, topic, payload):
        cb = None
        # Search if topic has a registered callback
        if topic in self.callbacks:
            cb = self.callbacks[topic]
        # else pick default callback
        else:
            cb = self.default_callback

        # Extract eventual indexing and grouping data from topic
        topic, opts = translate(topic)

        # check callback is valid and call
        if cb:
            cb(topic,payload, opts)
