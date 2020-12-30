#!/usr/bin/env python3

import argparse as ag
import os.path as path
import re

print("Attempting to set system76 keyboard backlight color and brightness.")

"""
Partially cribbed from
https://github.com/ahoneybun/keyboard-color-chooser/blob/master/keyboard-color-switcher.py

Called by 
/etc/systemd/system/system76-kb-backlight.service
as decribed here:
https://www.howtogeek.com/687970/how-to-run-a-linux-program-at-startup-with-systemd/

Example file /etc/systemd/system/system76-kb-backlight.service
```
[Unit]
Description=Set color and brightness of system-76 laptop keyboard backlight

[Service]
Type=simple
ExecStart=systemd-cat /home/makobates/.local/bin/set_system76_kb_backlight -g 55 -r FF -B 150

[Install]
WantedBy=multi-user.target
```
(Don't forget to enable the service.)
"""

def color_fragment(string):
    if re.fullmatch(r'^[0-9A-F]{2}$', string):
        return string
    else:
        raise ag.ArgumentTypeError(f'"{string}" is not a two-digit hex value.')

def brightness_fragment(string):
    if re.fullmatch(r'^[0-9]{1,3}$', string) and 0 <= int(string) and 255 >= int(string):
        return string
    else:
        raise ag.ArgumentTypeError(f'"{string}" is not an integer 0-255.')

arg_parse = ag.ArgumentParser(description="Set the color and brightness of the system76 keyboard backlight.")
arg_parse.add_argument('-r', help="The red RGB value (00 to FF).", default="00", type=color_fragment)
arg_parse.add_argument('-g', help="The green RGB value (00 to FF).", default="00", type=color_fragment)
arg_parse.add_argument('-b', help="The blue RGB value (00 to FF).", default="00", type=color_fragment)
arg_parse.add_argument('-B', help="The brightness (0 to 255).", default="48", type=brightness_fragment)

args = arg_parse.parse_args()
red = args.r
green = args.g
blue = args.b
brightness = args.B
color = f'{red}{green}{blue}'

ledPath = "/" + path.join('sys', 'class', 'leds', 'system76_acpi::kbd_backlight') + '/'
if not path.exists(ledPath):
    ledPath = "/" + path.join('sys', 'class', 'leds', 'system76::kbd_backlight') + '/'

regions = ['left', 'center', 'right', 'extra']
region_paths = [ledPath + f'color_{r}' for r in regions]
brightness_path = ledPath + 'brightness'
settings = {brightness_path: brightness,
            **{rp: color for rp in region_paths}}

for (p,s) in settings.items():
    with open(p, 'w') as f:
        f.write(s)

print("Successfully set system76 keyboard backlight brightness.")
arg_parse.exit(0)

