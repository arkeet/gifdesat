#!/usr/bin/env python

# Copyright (c) 2017 Adrian Keet
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys

if len(sys.argv) != 3:
    print('Usage: %s <INFILE> <OUTFILE>' % sys.argv[0])
    sys.exit(1)

infile = sys.argv[1]
outfile = sys.argv[2]

data = open(infile, 'rb').read()

if data[0:6] != b'GIF87a' and data[0:6] != b'GIF89a':
    print('Input is not a GIF file.')
    sys.exit(1)

if data[0xa] & 0x80 == 0:
    print('Global color map not found.')
    print('Note: local color tables aren\'t supported.')
    sys.exit(1)

color_count = 2 << (data[0xa] & 0x07)

data = list(data)
for i in range(color_count):
    offset = 0xd + 3*i
    r, g, b = data[offset : offset + 3]
    y = 0.299 * r + 0.587 * g + 0.114 * b
    y = int(y + 0.5)
    data[offset : offset + 3] = [y, y, y]

data = bytes(data)
open(outfile, 'wb').write(data)
