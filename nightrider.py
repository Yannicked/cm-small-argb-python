import pywinusb.hid as hid

import time

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

    try:
        while True:
            for i in range(14):
                colors = [0]*14*3
                colors[i*3] = 255

                led.set_colors(colors)
                time.sleep(0.05)
            for i in reversed(range(1,13)):
                colors = [0]*14*3
                colors[i*3] = 255

                led.set_colors(colors)
                time.sleep(0.05)
            
    except KeyboardInterrupt:
        pass

    #led.close()


if __name__ == '__main__':
    main()