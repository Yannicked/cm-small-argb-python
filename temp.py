import pywinusb.hid as hid

import wmi, math, threading

import time

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
    return [int(r), int(g), int(b)]

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

w = wmi.WMI(namespace="root\OpenHardwareMonitor")
def get_temperature():
    t = 0
    n = 0
    sensors = w.Sensor()
    for sensor in sensors:
        if sensor.SensorType == 'Temperature':
            if sensor.Name == 'GPU Core':
                t += sensor.Value
                n += 1
            if sensor.Name == 'CPU Package':
                t += sensor.Value
                n += 1
    
    return t/n




mintemp = 30
maxtemp = 65
temp = mintemp

def brighness_loop(output):
    global temp
    brightness = 0
    brightness_sin = 0
    while True:
        brightness_sin += 0.01
        brightness_sin %= 2 * math.pi
        brightness = math.sin(brightness_sin)**2 / 4 * 3 + 0.25
        r = int(max(0, min((temp)*2,1))*255)
        g = int(max(0, min(1-(temp-0.5)*2,1))*255)
        b = 0
        colors = create_static(r*brightness, g*brightness, b*brightness, 14)
        set_colors(output, colors)
        time.sleep(1/15)

def main():
    global temp
    target_vendor_id = 0x2516
    device = hid.HidDeviceFilter(vendor_id = target_vendor_id).get_devices()[0]
    #device.set_raw_data_handler(raw_handler)
    device.open()

    output = device.find_output_reports()[0]

    send_start(output)

    set_mode(output)
    t = threading.Thread(target=brighness_loop, args=(output,))
    t.start()
    try:
        while True:
            temp = get_temperature()
            print(f"Mean temp: {temp}")
            temp = max(temp - 30, 0)
            temp = min(temp/(maxtemp-mintemp), 1)
            # temp is now between 0 and 1 (mintemp-maxtemp)
            
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    device.close()


if __name__ == '__main__':
    main()