"""
    pytelemetry enables remote monitoring and program control. It is typically
    used to get readings and configure remotely an embedded device (Arduino,
    mbed, etc.) over a serial port.
    It is however fully hardware agnostic, and can be used for testing
    or for application development.
    The communication protocol is implemented in C, and new devices can be
    added in a matter of minutes.
"""
from pytelemetry.pytelemetry import Pytelemetry
