#!/usr/bin/env python3

import math
import argparse
import sys
import time

def mix(frequency, phase, middle, width, length):
    red =  math.sin(frequency * length + 0) * width + middle 
    green =  math.sin(frequency * length + (phase)) * width + middle 
    blue =  math.sin(frequency * length + (phase*2)) * width + middle
    return f'{int(red):02x}{int(green):02x}{int(blue):02x}' 

if __name__ == '__main__':

    example = 'Examples:\n\n'
    example += '$ .{} -f .3 --delay .25'.format(sys.argv[0]) 

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, epilog=example)

    sgroup = parser.add_argument_group("Main arguments")
    sgroup.add_argument("-f", metavar="FREQUENCY", dest='freq', default=.2, help='Frequency of the sine wave. Default is .2, higher value repeats faster.')
    sgroup.add_argument("--delay", metavar="SLEEP", dest='delay', default=.2, help='Take a breather between file writes. Really helps performance. Default .2s')
    args = parser.parse_args()

    frequency = float(args.freq)
    amplitude = 127
    middle = 128
    counter = 0
    
    phase_array = []

    for rgb in range(0,254):
        left_mix = mix(frequency, 2, middle, amplitude, rgb) 
        center_mix = mix(frequency, 2.5, middle, amplitude, rgb)
        right_mix = mix(frequency, 3.5, middle, amplitude, rgb)
        phase_array.append([left_mix, center_mix, right_mix])
        
    while True:
        for phase in phase_array:
            left_pane = phase[0]
            center_pane = phase[1]
            right_pane = phase[2]
            left = open('/sys/devices/platform/system76/leds/system76::kbd_backlight/color_left', 'w')
            left.write(left_pane)
            left.close()
            center =  open('/sys/devices/platform/system76/leds/system76::kbd_backlight/color_center', 'w')
            center.write(center_pane)
            center.close()
            right = open('/sys/devices/platform/system76/leds/system76::kbd_backlight/color_right', 'w')
            right.write(right_pane)
            right.close()
            counter+=1
            time.sleep(float(args.delay))
