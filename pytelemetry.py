from ctypes import *

# Function definitions for C api
buffer_operation_func_t =  CFUNCTYPE(c_int32, POINTER(c_uint8), c_uint32)
check_operation_func_t =  CFUNCTYPE(c_int32)

# transport struct definition for C api
class transportInterface(Structure):
    _fields_ = [("read", buffer_operation_func_t),
               ("readable", check_operation_func_t),
               ("write", buffer_operation_func_t),
               ("writeable", check_operation_func_t) ]

# user data struct for
class userDataStorage(Structure):
    _fields_ = [("count", c_uint32)]

# telemetry python wrapper
class pytelemetry:
    def __init__(self, transport):
        self.transport = transport
        self.callbacks = []

        self.api = CDLL('telemetry.dll')

        # Interface types definition
        self.api.init_telemetry.argtypes = [POINTER(userDataStorage),POINTER(transportInterface)]
        self.api.publish.argtypes = [c_char_p, c_char_p]

        # api initialization
        t = transportInterface(self.__read,self.__readable,self.__write,self.__writeable)
        u = userDataStorage(0)

        self.api.init_telemetry(byref(u),byref(t))

    def publish(self, topic, data, datatype):
        if datatype == 'string':
            self.api.publish(topic,data)

    # subscribe a callback to topic
    # Subscribing to None will call that function for any unsubscribed topic
    def subscribe(self, topic, cb):
        self.callbacks[topic] = cb

    def update(self):
        api.update_telemetry(0)

    @buffer_operation_func_t
    def __read(uint8_ptr, data_size):
        print("Trying to read at most ",data_size," characters.")
        return 0

    @buffer_operation_func_t
    def __write(uint8_t_ptr, data_size):
        print("Asking to write ",data_size," characters.")
        for i in range(data_size):
            print(uint8_t_ptr[i])
        return 0

    @check_operation_func_t
    def __readable():
        print("Asking is readable")
        return 0

    @check_operation_func_t
    def __writeable():
        print("Asking is writeable")
        return 1
