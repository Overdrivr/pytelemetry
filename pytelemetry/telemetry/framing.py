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
        self.SOF = 0xf7
        self.EOF = 0x7f
        self.ESC = 0x7d

        self.payload = bytearray()
        # Max amount of payloads
        self.framesize = 0;
        # new frame callback
        self.on_frame_decoded_callback = on_frame_decoded_callback

        self.resetStats()

    def resetStats(self):
        self.processed_rx_bytes = 0 # Total amount of processed RX bytes
        self.discarded_rx_bytes = 0 # Total amount of bytes received outside a delimited frame
        self.escaped_rx_bytes = 0 # Total amount of escaping characters inside received frames
        self.complete_rx_frames = 0 # Total amount of correctly delimited frames
        self.uncomplete_rx_frames = 0 # Total amount of badly delimited frames (frames that started by SOF but did not finish with EOF)

        self.processed_tx_bytes = 0 # Total amount of processed TX bytes
        self.encoded_tx_frames = 0 # Total amount of encoded frames
        self.escaped_tx_bytes = 0 # Total amount of escaping characters inside encoded frames

    def stats(self):
        return {
            "rx_processed_bytes"   : self.processed_rx_bytes,
            "rx_discarded_bytes"   : self.discarded_rx_bytes,
            "rx_escaped_bytes"     : self.escaped_rx_bytes,
            "rx_complete_frames"   : self.complete_rx_frames,
            "rx_uncomplete_frames" : self.uncomplete_rx_frames,
            "tx_processed_bytes"   : self.processed_tx_bytes,
            "tx_encoded_frames"    : self.encoded_tx_frames,
            "tx_escaped_bytes"     : self.escaped_tx_bytes
        }

    def decode(self, data):
        for c in data:
            self.processed_rx_bytes += 1

            # no frame in process
            if self.rx_state == RX_STATE.IDLE:
                if c == self.SOF:
                    # New frame started
                    self.rx_state = RX_STATE.IN_PROCESS
                    self.escape_state = ESC_STATE.IDLE
                    self.framesize = 0
                else:
                    self.discarded_rx_bytes += 1

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
                        self.complete_rx_frames += 1

                    elif c == self.SOF:
                        self.payload = bytearray()
                        self.rx_state = RX_STATE.IDLE
                        self.rx_state = RX_STATE.IN_PROCESS
                        self.framesize = 0
                        self.uncomplete_rx_frames += 1

                    # escape next
                    elif c == self.ESC:
                        self.escape_state = ESC_STATE.NEXT
                        self.escaped_rx_bytes += 1

                    # pure data
                    else:
                        self.payload.append(c)
                        self.framesize += 1;

    def encode(self,rxpayload):
        frame = bytearray()
        frame.append(self.SOF)

        self.encoded_tx_frames += 1

        for c in rxpayload:
            self.processed_tx_bytes += 1
            if c == self.SOF or c == self.EOF or c == self.ESC:
                frame.append(self.ESC)
                self.escaped_tx_bytes += 1
            frame.append(c)

        frame.append(self.EOF)

        return frame

    def get_processed_octets(self):
        return self.processed_octets
