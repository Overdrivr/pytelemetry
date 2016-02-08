from ctypes import *
import os

__all__ = ['Pytelemetry']

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
        self.transport = transport
        self.callbacks = dict()
        self.default_callback = None

        if telemetry_use_c_api:
            self.api = TelemetryCBinding(self._on_frame)
        else:
            self.api = Telemetry()

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

    def _on_frame(self, topic, payload)
        cb = None
        # Search if topic has a registered callback
        if topic in self.callbacks:
            cb = self.callbacks[topic]
        # else pick default callback
        else:
            cb = self.default_callback
        # check callback is valid
        if cb:
            cb(topic,payload)
