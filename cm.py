from ctypes import ArgumentError
import pywinusb.hid as hid
import threading

import time

class Led:
    def __init__(self):
        target_vendor_id = 0x2516
        self.device = hid.HidDeviceFilter(
            vendor_id=target_vendor_id).get_devices()[0]
        self.device.open()

        self.device.set_raw_data_handler(self.raw_data_handler)

        self.output = self.device.find_output_reports()[0]

        self.raw_data = b''

        self.wait_for_data = b'\x00\x80\x01\x01\x00\x03'
        self.wait_for_event = threading.Event()

        data = b'\x00\x80\x01\x01\x00\x01'
        self.send(data)

        assert(self.wait_for())

    def send(self, data):
        data += b'\x00'*(65-len(data))
        self.output.send(raw_data=data)

    def raw_data_handler(self, data):
        self.raw_data = bytes(data)
        if self.raw_data[0:len(self.wait_for_data)] == self.wait_for_data:
            self.wait_for_event.set()

    def ceildiv(a, b):  # Divide and ceil
        return -(-a // b)

    def set_led_count(self, num_leds):
        data = b'\x00\x80\x0d\x02\x01'
        checksum = Led.ceildiv(48, num_leds)
        data += bytes([checksum, num_leds])

        self.send(data)

    def wait_for(self, timeout=1):
        if not self.wait_for_event.wait(timeout):
            self.wait_for_event.clear()
            self.wait_for_data = b''
            return False
        
        self.wait_for_event.clear()
        self.wait_for_data = b''
        return True

    def send_hello(self):
        hello_pckt = b'\x00\x80\x01\x01\x00\x02'
        
        self.wait_for_data = b'\x00\x80\x01\x01\x00\x03'
        self.send(hello_pckt)

        assert(self.wait_for())

    def set_mode(self, mode, extradata=b'', wait_for_end=True):
        self.send_hello()

        data = b'\x00\x80\x0b\x02\x01'
        data += bytes([mode])
        data += extradata

        self.wait_for_data =  b'\x00\x80\x0b\x03\x00'
        self.wait_for_data += bytes([mode])

        self.send(data)

        assert(self.wait_for())
        if wait_for_end:
            self.wait_for_data = b'\x00\x80\x01\x01\x00\x03'
            assert(self.wait_for())

    def set_colors(self, colordata):
        self.set_mode(7, wait_for_end=False)
        colordata = bytes(colordata)
        colordata = colordata.ljust(48*3, b'\x00')[0:48*3]

        data = b'\x00\x00\x10\x02\x00'
        data += bytes([len(colordata)//3])
        data += colordata[0:(64-5)]
        
        self.wait_for_data = b'\x00\x80\x01\x01\x00\x03'
        self.send(data)
        assert(self.wait_for())

        data = b'\x00\x01'
        data += colordata[(3*20):(3*20 + 64-1)]
        self.send(data)

        data = b'\x00\x82'
        data += colordata[(3*20 + 64-1):(3*20 + 64 + 64-1)]
        self.send(data)

    def close(self):
        assert(False) # The device seems to crash more often if you do this
        self.device.close()
