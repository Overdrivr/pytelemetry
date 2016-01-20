from ctypes import *

# Function definitions for C api
buffer_operation_func_t =  CFUNCTYPE(c_int32_t, POINTER(c_uint8), c_uint32)
check_operation_func_t =  CFUNCTYPE(c_int32_t)

# transport struct definition for C api
class transportInterface:
    _field_ = [("read", buffer_operation_func_t),
               ("readable", check_operation_func_t),
               ("write", buffer_operation_func_t),
               ("writeable", check_operation_func_t) ]

@buffer_operation_func_t
def read(uint8_ptr, data_size):
    print("Trying to read at most ",data_size," characters.")
    return 0

@buffer_operation_func_t
def write(uint8_t_ptr, data_size):
    print("Asking to write ",data_size," characters.")
    return 0

@check_operation_func_t
def readable():
    print("Asking is readable")
    return 0

@check_operation_func_t
def writeable():
    print("Asking is writeable")
    return 0

# telemetry python wrapper
class pytelemetry:
    def __init__(self, transport):
        self.transport = transport
        self.callbacks = []

        self.api = CDLL('telemetry.dll')

    def publish(self, topic, data, datatype):
        pass

    # subscribe a callback to topic
    # Subscribing to None will call that function for any unsubscribed topic
    def subscribe(self, topic, cb):
        self.callbacks[topic] = cb

    def update(self):
        pass
