class SerialTransport:
    def __init__(self):
        pass

    # The transport interface

    def read(self, maxbytes=1):
        print("Trying to read at most ",maxbytes," characters.")
        return 0 # TODO: Return char instead

    def readable(self):
        return 0

    def write(self, data):
        print("Asking to write ",data)
        return 0

    def writeable(self):
        return 1
