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

    def decode(self, rxbyte):
        #newbyte = int.from_bytes(rxbyte,byteorder='big')
        newbyte=rxbyte
        #newbyte = rxbyte
        self.processed_octets += 1
        #No frame in process
        if self.rx_state == RX_STATE.IDLE:
            if newbyte == self.SOF:
                # New frame started
                self.rx_state = RX_STATE.IN_PROCESS
                self.escape_state = ESC_STATE.IDLE
                self.framesize = 0;
            else:
                pass
                #print(str(newbyte))

        #Frame is in process
        else:
            #Next char must be data
            if self.escape_state == ESC_STATE.NEXT:
                #Byte destuffing, this char must not be interpreted as flag
                #See serial_protocols_definition.xlsx
                self.payload.append(newbyte)
                self.escape_state = ESC_STATE.IDLE
                self.framesize += 1;

            #Next char can be data or flag (EOF, SOF,..)
            elif self.escape_state == ESC_STATE.IDLE:
                #End of frame, the payload is immediatly send to callback function
                if newbyte == self.EOF:
                    # Send frame to callback function
                    self.on_frame_decoded_callback(self.payload)
                    self.payload = bytearray()
                    self.rx_state = RX_STATE.IDLE

                #Receive a SOF while a frame is running, error
                elif newbyte == self.SOF:
                    #print("Protocol : Received frame unvalid, discarding.", self.payload)
                    self.payload = bytearray()
                    self.rx_state = RX_STATE.IDLE

                #Escaping
                elif newbyte == self.ESC:
                    self.escape_state = ESC_STATE.NEXT

                #Storing data
                else:
                    self.payload.append(newbyte)
                    self.framesize += 1;
            else:
                pass
                #print("Unprocessed :"+str(newbyte))

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
