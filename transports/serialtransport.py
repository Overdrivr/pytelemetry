class SerialTransport:
    def __init__(self):
        pass

    # The transport interface

    def read(self, maxbytes=1):
        print("Trying to read at most ",maxbytes," characters.")
        return 0 # TODO: Return char instead

    def readable(self):
        pass

    def write(self, data):
        print("Asking to write ",data)

    def writeable(self):
        pass
