#!/usr/bin/env python3
#
# A script to strip the tracking cookies from Twitter links in your clipboard.
# Also strips other tracking parameters.
#

import pasteboard
import time

pb = pasteboard.Pasteboard()

while True:
    str = pb.get_contents()
    orig = str
    if str is not None and str.startswith('https://twitter.com/') and str.find('t=') != -1:
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
        print ("reset " + orig + " to " + str)

    time.sleep (0.5)
