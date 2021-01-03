import pywinusb.hid as hid

import time

import colorsys

def send_start(output):
    data = b'\x00\x80\x01\x01\x00\x01'
    data += b'\x00'*(65-len(data))

    output.send(raw_data = data)

def send_end(output):
    data = b'\x00\x01'
    data += b'\x00'*(65-len(data))

    output.send(raw_data = data)

    data = b'\x00\x82'
    data += b'\x00'*(65-len(data))

    output.send(raw_data = data)

def set_colors(output, colordata):
    # r g b, r g b, r g b
    data = b'\x00\x00\x10\x02\x00\x30'
    data += bytes(colordata)

    data += b'\x00'*(65-len(data))

    output.send(raw_data = data)
    
    send_end(output)

def make_rgb(r, g, b):
    return [r, g, b]

def create_static(r, g, b, num):
    ret = []

    for _ in range(num):
        ret += make_rgb(r, g, b)

    return ret

def set_mode(output):
    data = b'\x00\x80\x0b\x02\x01\x07'
    data += b'\x00'*(65-len(data))

    output.send(raw_data = data)

def raw_handler(data):
    print("Raw data: {0}".format(data))

def main():
    target_vendor_id = 0x2516
    device = hid.HidDeviceFilter(vendor_id = target_vendor_id).get_devices()[0]
    #device.set_raw_data_handler(raw_handler)
    device.open()

    output = device.find_output_reports()[0]

    #set_led_amount(output, 14)
    #send_meuk(output)

    send_start(output)

    set_mode(output)

    while True:
        for angle in range(0, 100, 2):
            colors = []
            for led in range(14):
                h = (angle + 100/14*led % 100)/100
                s = 1
                v = 1
                r,g,b = colorsys.hsv_to_rgb(h,s,v)
                colors += make_rgb(int(r*255),int(g*255),int(b*255))
            set_colors(output, colors)
            time.sleep(1/15)

    device.close()


if __name__ == '__main__':
    main()