#!/usr/bin/env python

""" Python implementation of ASCII85/ASCIIHex decoder (Adobe version).

This code is in the public domain.

"""

"""
MIT License

Copyright (c) 2004-2019  Yusuke Shinyama

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""


import re
import struct


# ascii85decode(data)
def ascii85decode(data):
    """
    In ASCII85 encoding, every four bytes are encoded with five ASCII
    letters, using 85 different types of characters (as 256**4 < 85**5).
    When the length of the original bytes is not a multiple of 4, a special
    rule is used for round up.

    The Adobe's ASCII85 implementation is slightly different from
    its original in handling the last characters.

    The sample string is taken from:
      http://en.wikipedia.org/w/index.php?title=Ascii85

    >>> ascii85decode(b'9jqo^BlbD-BleB1DJ+*+F(f,q')
    b'Man is distinguished'
    >>> ascii85decode(b'E,9)oF*2M7/c~>')
    b'pleasure.'
    """
    n = b = 0
    out = b''
    for c in data:
        if 33 <= c and c <= 117: # b'!' <= c and c <= b'u'
            n += 1
            b = b*85+(c-33)
            if n == 5:
                out += struct.pack('>L', b)
                n = b = 0
        elif c == 122: # b'z'
            assert n == 0
            out += b'\0\0\0\0'
        elif c == 126: # b'~'
            if n:
                for _ in range(5-n):
                    b = b*85+84
                out += struct.pack('>L', b)[:n-1]
            break
    return out

# asciihexdecode(data)
hex_re = re.compile(r'([a-f\d]{2})', re.IGNORECASE)
trail_re = re.compile(r'^(?:[a-f\d]{2}|\s)*([a-f\d])[\s>]*$', re.IGNORECASE)


def asciihexdecode(data):
    """
    ASCIIHexDecode filter: PDFReference v1.4 section 3.3.1
    For each pair of ASCII hexadecimal digits (0-9 and A-F or a-f), the
    ASCIIHexDecode filter produces one byte of binary data. All white-space
    characters are ignored. A right angle bracket character (>) indicates
    EOD. Any other characters will cause an error. If the filter encounters
    the EOD marker after reading an odd number of hexadecimal digits, it
    will behave as if a 0 followed the last digit.

    >>> asciihexdecode(b'61 62 2e6364   65')
    b'ab.cde'
    >>> asciihexdecode(b'61 62 2e6364   657>')
    b'ab.cdep'
    >>> asciihexdecode(b'7>')
    b'p'
    """
    data = data.decode('latin1')
    out = [ int(hx,16) for hx in  hex_re.findall(data) ]
    m = trail_re.search(data)
    if m:
        out.append(int(m.group(1),16) << 4)
    return bytes(out)


if __name__ == '__main__':
    import doctest
    print('pdfminer.ascii85', doctest.testmod())