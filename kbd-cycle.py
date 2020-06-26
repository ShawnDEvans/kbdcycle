#!/usr/bin/env python3

import math

def mix(frequency, phase, middle, width, length, pane_phase):
    red =  math.sin(frequency * length + 0 + pane_phase) * width + middle 
    green =  math.sin(frequency * length + (phase) + pane_phase) * width + middle 
    blue =  math.sin(frequency * length + (phase*2) + pane_phase) * width + middle
    return f'{int(red):02x}{int(green):02x}{int(blue):02x}' 

if __name__ == '__main__':

    frequency = .025
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
        center = open('/sys/devices/platform/system76/leds/system76::kbd_backlight/color_center', 'w')
        center.write(center_mix)
        center.close()
        right = open('/sys/devices/platform/system76/leds/system76::kbd_backlight/color_right', 'w')
        right.write(right_mix)
        right.close()
        if counter > 255:
            counter = 0
        counter+=1
