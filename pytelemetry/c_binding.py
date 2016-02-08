
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

class TelemetryCBinding:
    """
C API Abstraction over the C binding protocol implementation
    """
    def __init__(self, on_frame_callback):

        self.on_frame_callback = on_frame_callback

        lib_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'telemetry','telemetry.dll')
        lib_crc16 = os.path.join(os.path.dirname(os.path.dirname(__file__)),'telemetry','crc16.dll')
        lib_framing = os.path.join(os.path.dirname(os.path.dirname(__file__)),'telemetry','framing.dll')

        self.crc16 = CDLL(lib_crc16)
        self.framing = CDLL(lib_framing)
        self.api = CDLL(lib_path)

        # Interface types definition
        self.api.init_telemetry.argtypes = [POINTER(TM_state),POINTER(TM_transport)]
        self.api.publish.argtypes = [c_char_p, c_char_p]
        self.api.publish_u8.argtypes = [c_char_p, c_uint8]
        self.api.publish_u16.argtypes = [c_char_p, c_uint16]
        self.api.publish_u32.argtypes = [c_char_p, c_uint32]
        self.api.publish_i8.argtypes = [c_char_p, c_int8]
        self.api.publish_i16.argtypes = [c_char_p, c_int16]
        self.api.publish_i32.argtypes = [c_char_p, c_int32]
        self.api.publish_f32.argtypes = [c_char_p, c_float]

        self.api.update_telemetry.argtypes = [c_float]

        self.api.emplace.argtypes = [POINTER(TM_msg),c_char_p,c_uint32]
        self.api.emplace_u8.argtypes = [POINTER(TM_msg),POINTER(c_uint8)]
        self.api.emplace_u16.argtypes = [POINTER(TM_msg),POINTER(c_uint16)]
        self.api.emplace_u32.argtypes = [POINTER(TM_msg),POINTER(c_uint32)]
        self.api.emplace_i8.argtypes = [POINTER(TM_msg),POINTER(c_int8)]
        self.api.emplace_i16.argtypes = [POINTER(TM_msg),POINTER(c_int16)]
        self.api.emplace_i32.argtypes = [POINTER(TM_msg),POINTER(c_int32)]
        self.api.emplace_f32.argtypes = [POINTER(TM_msg),POINTER(c_float)]

        # Storing closures for C API callback
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

    def update(self):
        self.api.update_telemetry(0)

    def publish(self, topic, data, datatype):
        """

        """
        if datatype == 'string':
            self.api.publish(topic.encode(encoding='ascii'),data.encode(encoding='ascii'))
        elif datatype == 'uint8':
            self.api.publish_u8(topic.encode(encoding='ascii'), data)
        elif datatype == 'uint16':
            self.api.publish_u16(topic.encode(encoding='ascii'), data)
        elif datatype == 'uint32':
            self.api.publish_u32(topic.encode(encoding='ascii'), data)
        elif datatype == 'int8':
            self.api.publish_i8(topic.encode(encoding='ascii'), data)
        elif datatype == 'int16':
            self.api.publish_i16(topic.encode(encoding='ascii'), data)
        elif datatype == 'int32':
            self.api.publish_i32(topic.encode(encoding='ascii'), data)
        elif datatype == 'float32':
            self.api.publish_f32(topic.encode(encoding='ascii'), data)

    def __get_on_frame_cb(self):
        def on_frame(state,msg):
            topic = msg.contents.topic.decode(encoding='utf-8')
            payload = None
            # cast buffer to string
            if msg.contents.type == 7 :
                # Create a char * (+ 1 to have enough space)
                cbuf = create_string_buffer(msg.contents.size + 1)
                # Use api to format data correctly
                self.api.emplace(msg,cbuf,msg.contents.size + 1)
                # Convert bytes code to utf-8
                payload = cbuf.value.decode('utf-8')

            # cast buffer to uint8
            elif msg.contents.type == 1 :
                cbuf = c_uint8()
                # Use api to format data correctly
                self.api.emplace_u8(msg,byref(cbuf))
                # Store decoded data
                payload = cbuf.value

            # cast buffer to uint16
            elif msg.contents.type == 2 :
                cbuf = c_uint16()
                # Use api to format data correctly
                self.api.emplace_u16(msg,byref(cbuf))
                # Store decoded data
                payload = cbuf.value

            # cast buffer to uint32
            elif msg.contents.type == 3 :
                cbuf = c_uint32()
                # Use api to format data correctly
                self.api.emplace_u32(msg,byref(cbuf))
                # Store decoded data
                payload = cbuf.value

            # cast buffer to int8
            elif msg.contents.type == 4 :
                cbuf = c_int8()
                # Use api to format data correctly
                self.api.emplace_i8(msg,byref(cbuf))
                # Store decoded data
                payload = cbuf.value

            # cast buffer to int16
            elif msg.contents.type == 5 :
                cbuf = c_int16()
                # Use api to format data correctly
                self.api.emplace_i16(msg,byref(cbuf))
                # Store decoded data
                payload = cbuf.value

            # cast buffer to int32
            elif msg.contents.type == 6 :
                # Create a int32
                cbuf = c_int32()
                # Use api to format data correctly
                self.api.emplace_i32(msg,byref(cbuf))
                # Store decoded data
                payload = cbuf.value

            # cast buffer to float32
            elif msg.contents.type == 0 :
                # Create a int32
                cbuf = c_float()
                # Use api to format data correctly
                self.api.emplace_f32(msg,byref(cbuf))
                # Store decoded data
                payload = cbuf.value

            self.on_frame_callback(topic,payload)
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
