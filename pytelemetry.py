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

        # Storing closures
        # See http://stackoverflow.com/questions/7259794/how-can-i-get-methods-to-work-as-callbacks-with-python-ctypes
        self.__read = self.__get_read_cb()
        self.__write = self.__get_write_cb()
        self.__readable = self.__get_readable_cb()
        self.__writeable = self.__get_writeable_cb()

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

    def __get_read_cb(self):
        def read(uint8_ptr, data_size):
            # Read the data
            data = self.transport.read(maxbytes=data_size)
            # TODO :Emplace it into the ptr

            # TODO :Return actual amount of read characters
            return 0
        return buffer_operation_func_t(read)

    def __get_write_cb(self):
        def write(uint8_t_ptr, data_size):
            for i in range(data_size):
                self.transport.write(uint8_t_ptr[i])
            return 0
        return buffer_operation_func_t(write)

    def __get_readable_cb(self):
        def readable():
            return self.transport.readable()
        return check_operation_func_t(readable)

    def __get_writeable_cb(self):
        def writeable():
            return self.transport.writeable()
        return check_operation_func_t(writeable)
