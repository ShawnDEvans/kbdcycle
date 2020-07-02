#!/usr/bin/env python3

import math
import argparse
import sys
import time

DARTER = '/sys/class/leds/system76_acpi::kbd_backlight'
ORYX = '/sys/devices/platform/system76/leds/system76::kbd_backlight'

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
    sgroup.add_argument("--left", metavar="PHASE", dest='left_phase', default=1, help='Phase shift of left pane, default 1')
    sgroup.add_argument("--center", metavar="PHASE", dest='center_phase', default=2, help='Phase shift of center pane, default 2')
    sgroup.add_argument("--right", metavar="PHASE", dest='right_phase', default=3, help='Phase shift of right pane, default 3')
    sgroup.add_argument("--darter", dest='darter', default=False, action='store_true', help='Engages Darter pro mode, which has a single color pane')
    args = parser.parse_args()

    frequency = float(args.freq)
    amplitude = 127
    middle = 128
    
    phase_array = []
    
    path = ORYX
    if args.darter:
        path = DARTER

    for rgb in range(1,255):
        if args.darter:
            darter_mix = mix(frequency, 1, middle, amplitude, rgb)
            phase_array.append([darter_mix])
        else:
            left_mix = mix(frequency, args.left_phase, middle, amplitude, rgb) 
            center_mix = mix(frequency, args.center_phase,middle, amplitude, rgb)
            right_mix = mix(frequency, args.right_phase, middle, amplitude, rgb)
            phase_array.append([left_mix, center_mix, right_mix])
        
    while True:
        try:
            if args.darter:
                for phase in phase_array:
                    pane = phase[0]
                    darter_pane = open('{}/color'.format(path), 'w')
                    darter_pane.write(pane)
                    darter_pane.close()
                    time.sleep(float(args.delay))
            else:
                for phase in phase_array:
                    left_pane = phase[0]
                    center_pane = phase[1]
                    right_pane = phase[2]
                    left = open('{}/color_left'.format(path), 'w')
                    left.write(left_pane)
                    left.close()
                    center =  open('{}/color_center'.format(path), 'w')
                    center.write(center_pane)
                    center.close()
                    right = open('{}/color_right'.format(path), 'w')
                    right.write(right_pane)
                    right.close()
                    time.sleep(float(args.delay))
        except FileNotFoundError as e:
            print('[!] Looks like your system doesn\'t have the file: ', e.filename)
            print('[!] Default is set for Oryx Pro, try --darter if you\'re using a Darter')
            print('[!] If you have a different model with color KB, log an issue: https://github.com/ShawnDEvans/kbdcycle')
            sys.exit()
