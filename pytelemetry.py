from ctypes import *

# Function definitions for C api
buffer_operation_func_t = CFUNCTYPE(c_int32, POINTER(c_uint8), c_uint32)
check_operation_func_t = CFUNCTYPE(c_int32)

# transport struct definition for C api
class TM_transport(Structure):
    _fields_ = [("read", buffer_operation_func_t),
               ("readable", check_operation_func_t),
               ("write", buffer_operation_func_t),
               ("writeable", check_operation_func_t) ]

# user data struct for
class TM_state(Structure):
    _fields_ = [("count", c_uint32)]

class TM_msg(Structure):
    _fields_ = [("type", c_uint32),# WARNING : No way of telling it's actually uin32
                ("topic", c_char_p),
                ("buffer", POINTER(c_uint8)),
                ("size", c_uint32)]

on_frame_callback_t = CFUNCTYPE(None,POINTER(TM_state),POINTER(TM_msg))

# telemetry python wrapper
class pytelemetry:
    def __init__(self, transport):
        self.transport = transport
        self.callbacks = dict()
        self.default_callback = None
        self.api = CDLL('telemetry.dll')

        # Interface types definition
        self.api.init_telemetry.argtypes = [POINTER(TM_state),POINTER(TM_transport)]
        self.api.publish.argtypes = [c_char_p, c_char_p]
        self.api.publish_u8.argtypes = [c_char_p, c_uint8]

        self.api.update_telemetry.argtypes = [c_float]

        self.api.emplace.argtypes = [POINTER(TM_msg),c_char_p,c_uint32]
        self.api.emplace_u8.argtypes = [POINTER(TM_msg),POINTER(c_uint8)]

        # Storing closures
        # See http://stackoverflow.com/questions/7259794/how-can-i-get-methods-to-work-as-callbacks-with-python-ctypes
        self.__read = self.__get_read_cb()
        self.__write = self.__get_write_cb()
        self.__readable = self.__get_readable_cb()
        self.__writeable = self.__get_writeable_cb()
        self.__on_frame = self.__get_on_frame_cb()

        # api initialization - store t and u to avoid garbage collection
        self.t = TM_transport(self.__read,self.__readable,self.__write,self.__writeable)
        self.u = TM_state(0)

        self.api.init_telemetry(byref(self.u),byref(self.t))
        self.api.subscribe(self.__on_frame)

    def publish(self, topic, data, datatype):
        if datatype == 'string':
            self.api.publish(topic.encode(encoding='ascii'),data.encode(encoding='ascii'))
        elif datatype == 'uint8':
            self.api.publish_u8(topic.encode(encoding='ascii'), data)
            

    # subscribe a callback to topic
    # Subscribing to None will call that function for any unsubscribed topic
    def subscribe(self, topic, cb):
        if topic:
            self.callbacks[topic] = cb
        else:
            self.default_callback = cb

    def update(self):
        self.api.update_telemetry(0)

    def __get_on_frame_cb(self):
        def on_frame(state,msg):
            topic = msg.contents.topic.decode(encoding='utf-8')
            cb = None
            # Search if topic has a registered callback
            if topic in self.callbacks:
                cb = self.callbacks[topic]
            # else pick default callback
            else:
                cb = self.default_callback

            # TODO cast buffer to appropriate type
            payload = None
            if msg.contents.type == 7 :
                # Create a char * (+ 1 to have enough space)
                cbuf = create_string_buffer(msg.contents.size + 1)
                # Use api to format data correctly
                self.api.emplace(msg,cbuf,msg.contents.size + 1)
                # Convert bytes code to utf-8
                payload = cbuf.value.decode('utf-8')
            elif msg.contents.type == 1 :
                # Create a uint8
                cbuf = c_uint8()
                # Use api to format data correctly
                self.api.emplace_u8(msg,byref(cbuf))
                # Store decoded data
                payload = cbuf.value

            # check callback is valid
            if cb:
                cb(topic,payload)
        return on_frame_callback_t(on_frame)

    def __get_read_cb(self):
        def read(uint8_ptr, data_size):
            # Read the data
            data = self.transport.read(maxbytes=data_size)

            if len(data) > data_size:
                return 0

            for i in range(len(data)):
                uint8_ptr[i] = data[i]

            return len(data)
        return buffer_operation_func_t(read)

    def __get_write_cb(self):
        def write(uint8_t_ptr, data_size):
            data = []
            for i in range(data_size):
                data.append(uint8_t_ptr[i])
            self.transport.write(data)
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
