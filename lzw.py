#!/usr/bin/env python
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


from io import BytesIO


class CorruptDataError(Exception):
    pass


##  LZWDecoder
##
class LZWDecoder:

    def __init__(self, fp):
        self.fp = fp
        self.buff = 0
        self.bpos = 8
        self.nbits = 9
        self.table = None
        self.prevbuf = None
        return

    def readbits(self, bits):
        v = 0
        while 1:
            # the number of remaining bits we can get from the current buffer.
            r = 8-self.bpos
            if bits <= r:
                # |-----8-bits-----|
                # |-bpos-|-bits-|  |
                # |      |----r----|
                v = (v << bits) | ((self.buff >> (r-bits)) & ((1 << bits)-1))
                self.bpos += bits
                break
            else:
                # |-----8-bits-----|
                # |-bpos-|---bits----...
                # |      |----r----|
                v = (v << r) | (self.buff & ((1 << r)-1))
                bits -= r
                x = self.fp.read(1)
                if not x:
                    raise EOFError
                self.buff = x[0]
                self.bpos = 0
        return v

    def feed(self, code):
        x = b''
        if code == 256:
            self.table = [bytes([c]) for c in range(256)]  # 0-255
            self.table.append(None)  # 256
            self.table.append(None)  # 257
            self.prevbuf = b''
            self.nbits = 9
        elif code == 257:
            pass
        elif not self.prevbuf:
            x = self.prevbuf = self.table[code]
        else:
            if code < len(self.table):
                x = self.table[code]
                self.table.append(self.prevbuf+x[:1])
            elif code == len(self.table):
                self.table.append(self.prevbuf+self.prevbuf[:1])
                x = self.table[code]
            else:
                raise CorruptDataError
            l = len(self.table)
            if l == 511:
                self.nbits = 10
            elif l == 1023:
                self.nbits = 11
            elif l == 2047:
                self.nbits = 12
            self.prevbuf = x
        return x

    def run(self):
        while 1:
            try:
                code = self.readbits(self.nbits)
            except EOFError:
                break
            try:
                x = self.feed(code)
            except CorruptDataError:
                # just ignore corrupt data and stop yielding there
                break
            yield x
            #logging.debug('nbits=%d, code=%d, output=%r, table=%r' %
            #              (self.nbits, code, x, self.table[258:]))
        return


# lzwdecode
def lzwdecode(data):
    """
    >>> lzwdecode(bytes.fromhex('800b6050220c0c8501'))
    b'-----A---B'
    """
    fp = BytesIO(data)
    return b''.join(LZWDecoder(fp).run())

if __name__ == '__main__':
    import doctest
    print('pdfminer.lzw', doctest.testmod())
