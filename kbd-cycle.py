#!/usr/bin/env python3

import math
import argparse
import sys
import time

def mix(frequency, phase, middle, width, length, pane_phase):
    red =  math.sin(frequency * length + 0 + pane_phase) * width + middle 
    green =  math.sin(frequency * length + (phase) + pane_phase) * width + middle 
    blue =  math.sin(frequency * length + (phase*2) + pane_phase) * width + middle
    return f'{int(red):02x}{int(green):02x}{int(blue):02x}' 

if __name__ == '__main__':

    example = 'Examples:\n\n'
    example += '$ .{}'.format(sys.argv[0]) 

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, epilog=example)

    sgroup = parser.add_argument_group("Main arguments")
    sgroup.add_argument("-f", metavar="FREQUENCY", dest='freq', default=.2, help='Frequency of the sine wave. Default is .2, higher value repeats faster.')
    sgroup.add_argument("--delay", metavar="SLEEP0", dest='delay', default=.2, help='Take a breather between file writes. Really helps performance. Default .2s')
    args = parser.parse_args()

    frequency = float(args.freq)
    amplitude = 127
    middle = 128
    counter = 0

    while True:
        left_mix = mix(frequency, 2, middle, amplitude, counter, 0) 
        center_mix = mix(frequency, 2, middle, amplitude, counter, .5)
        right_mix = mix(frequency, 2, middle, amplitude, counter, 1)
        left = open('/sys/devices/platform/system76/leds/system76::kbd_backlight/color_left', 'w')
        left.write(left_mix)
        left.close()
        center =  open('/sys/devices/platform/system76/leds/system76::kbd_backlight/color_center', 'w')
        center.write(center_mix)
        center.close()
        right = open('/sys/devices/platform/system76/leds/system76::kbd_backlight/color_right', 'w')
        right.write(right_mix)
        right.close()
        counter+=1
        time.sleep(float(args.delay))
        if counter > 255:
            counter = 0
