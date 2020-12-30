#!/usr/bin/env python3

#import argparse as ag
#from glob import iglob
#from operator import itemgetter
import os.path as path
#import re
#import subprocess
import sys

print("Attempting to set system76 keyboard backlight brightness.")

"""
substantially cribbed from
https://github.com/ahoneybun/keyboard-color-chooser/blob/master/keyboard-color-switcher.py

called by /etc/systemd/system/system76-kb-backlight.service
per https://www.howtogeek.com/687970/how-to-run-a-linux-program-at-startup-with-systemd/
"""

"""def log(message, is_error):
    subprocess.run(['systemd-cat', '-p', info])"""


ledPath = "/" + path.join('sys', 'class', 'leds', 'system76_acpi::kbd_backlight') + '/'
if not path.exists(ledPath):
    ledPath = "/" + path.join('sys', 'class', 'leds', 'system76::kbd_backlight') + '/'

regions = ['left', 'center', 'right', 'extra']
r_paths = [ledPath + f'color_{r}' for r in regions]
b_path = ledPath + 'brightness'

color = 'FF0000'
brightness = '10'

settings = dict([(b_path, brightness), *((rp, color) for rp in r_paths)])

for (p,s) in settings.items():
    with open(p, 'w') as f:
        f.write(s)

print("Successfully set system76 keyboard backlight brightness.")
sys.exit(0)

