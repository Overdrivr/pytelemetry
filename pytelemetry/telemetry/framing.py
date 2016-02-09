# Copyright (C) 2014 Rémi Bèges
# For conditions of distribution and use, see copyright notice in the LICENSE file

from enum import Enum
from queue import Queue

class RX_STATE(Enum):
    IDLE = 0
    IN_PROCESS = 1

class ESC_STATE(Enum):
    IDLE = 0
    NEXT = 1

class Delimiter():
    def __init__(self,on_frame_decoded_callback):
        self.rx_state = RX_STATE.IDLE;
        self.escape_state = ESC_STATE.IDLE;
        self.SOF = int('f7',16)
        self.EOF = int('7f',16)
        self.ESC = int('7d',16)

        self.payload = bytearray()
        # Max amount of payloads
        self.framesize = 0;
        self.processed_octets = 0
        # new frame callback
        self.on_frame_decoded_callback = on_frame_decoded_callback

    def decode(self, data):
        for c in data:
            self.processed_octets += 1
            # no frame in process
            if self.rx_state == RX_STATE.IDLE:
                if c == self.SOF:
                    # New frame started
                    self.rx_state = RX_STATE.IN_PROCESS
                    self.escape_state = ESC_STATE.IDLE
                    self.framesize = 0

            # frame in process
            else:
                # escaping
                if self.escape_state == ESC_STATE.NEXT:
                    self.payload.append(c)
                    self.escape_state = ESC_STATE.IDLE
                    self.framesize += 1;

                elif self.escape_state == ESC_STATE.IDLE:
                    if c == self.EOF:
                        # Send frame to callback function
                        self.on_frame_decoded_callback(self.payload)
                        self.payload = bytearray()
                        self.rx_state = RX_STATE.IDLE

                    elif c == self.SOF:
                        self.payload = bytearray()
                        self.rx_state = RX_STATE.IDLE
                        self.rx_state = RX_STATE.IN_PROCESS
                        self.framesize = 0

                    # escape next
                    elif c == self.ESC:
                        self.escape_state = ESC_STATE.NEXT

                    # pure data
                    else:
                        self.payload.append(c)
                        self.framesize += 1;

    def encode(self,rxpayload):
        frame = bytearray()
        frame.append(self.SOF)

        for c in rxpayload:
            if c == self.SOF or c == self.EOF or c == self.ESC:
                frame.append(self.ESC)
            frame.append(c)

        frame.append(self.EOF)

        return frame

    def get_processed_octets(self):
        return self.processed_octets
