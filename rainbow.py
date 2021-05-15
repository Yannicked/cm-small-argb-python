import pywinusb.hid as hid

import time

import colorsys

from cm import Led

def make_rgb(r, g, b):
    return [r, g, b]

def create_static(r, g, b, num):
    ret = []

    for _ in range(num):
        ret += make_rgb(r, g, b)

    return ret

def main():
    
    led = Led()
    led.set_led_count(14)
    led.set_mode(7)

    while True:
        for angle in range(0, 100, 2):
            colors = []
            for l in range(14):
                h = (angle + 100/14*l % 100)/100
                s = 1
                v = 1
                r,g,b = colorsys.hsv_to_rgb(h,s,v)
                colors += make_rgb(int(r*255),int(g*255),int(b*255))
            led.set_colors(colors)
            time.sleep(1/30)


if __name__ == '__main__':
    main()