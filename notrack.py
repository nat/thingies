#!/usr/bin/env python3
#
# A script to strip the tracking cookies from Twitter links in your clipboard.
# Also strips other tracking parameters.
#

import pasteboard
import difflib
import time

red = lambda text: f"\033[31m{text}\033[0m"
green = lambda text: f"\033[32m{text}\033[0m"
blue = lambda text: f"\033[34m{text}\033[0m"
white = lambda text: f"\033[37m{text}\033[0m"

def string_diff(old, new):
    result = ""
    codes = difflib.SequenceMatcher(a=old, b=new).get_opcodes()
    for code in codes:
        if code[0] == "equal": 
            result += white(old[code[1]:code[2]])
        elif code[0] == "delete":
            result += red(old[code[1]:code[2]])
        elif code[0] == "insert":
            result += green(new[code[3]:code[4]])
        elif code[0] == "replace":
            result += (red(old[code[1]:code[2]]) + green(new[code[3]:code[4]]))
    return result

pb = pasteboard.Pasteboard()

while True:
    str = pb.get_contents()
    if str is not None:
        orig = str
        if str.startswith('https://twitter.com/') and str.find('t=') != -1:
            str = str.split('?')[0]
            pb.set_contents(str)

        if str.startswith('http') and (str.find('utm_') != -1 or str.find('st=') != -1 or str.find('reflink') != -1):
            params = str.split('?')[1]
            params = params.split('&')
            params = [x for x in params if not x.startswith('utm_') and not x.startswith('reflink') and not x.startswith('st=')]
            params = '&'.join(params)
            str = str.split('?')[0] + ('?' + params if len(params) > 0 else '')
            pb.set_contents(str)
        
        if str != orig:
            print(string_diff(orig, str))

    time.sleep (0.5)
