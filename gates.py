# SPOILER WARNING! HERE ARE SOLUTIONS TO THE CHAPTER 1 PROBLEMS.
# DO NOT READ THIS IF YOU WANT TO SOLVE THEM FOR YOURSELF.

import logsim
from logsim import Wire, nand, false, wires
import simtest


def test_not():
    in_ = Wire()
    out = ~in_
    simtest.test(locals(), 'tests/1/Not.tst')

def not_(a):
    return nand(a, a)


def test_and():
    a = Wire()
    b = Wire()
    out = a & b
    simtest.test(locals(), 'tests/1/And.tst')

def and_(a, b):
    return ~nand(a, b)


def test_or():
    a = Wire()
    b = Wire()
    out = a | b
    simtest.test(locals(), 'tests/1/Or.tst')

def or_(a, b):
    return nand(~a, ~b)


def test_xor():
    a = Wire()
    b = Wire()
    out = a ^ b
    simtest.test(locals(), 'tests/1/Xor.tst')

def xor(a, b):
    return nand(nand(a, ~b),
                nand(~a, b))


def test_mux():
    a = Wire()
    b = Wire()
    sel = Wire()
    out = mux(a, b, sel)
    simtest.test(locals(), 'tests/1/Mux.tst')

def mux(a, b, sel):
    "if sel=0 then a else b"
    # TODO: use nands directly and save a few gates
    return (~sel & a) | (sel & b)


def test_dmux():
    in_ = Wire()
    sel = Wire()
    a, b = dmux(in_, sel)
    simtest.test(locals(), 'tests/1/DMux.tst')

def dmux(in_, sel):
    "if sel=0 then (in,0) else (0,in)"
    return (mux(in_, false, sel),
            mux(false, in_, sel))


def test_not16():
    in_ = wires(16)
    out = not16(in_)
    simtest.test(locals(), 'tests/1/Not16.tst')

def not16(in_):
    "16-wide NOT"
    return tuple(~w for w in in_)


def test_and16():
    a = wires(16)
    b = wires(16)
    out = and16(a, b)
    simtest.test(locals(), 'tests/1/And16.tst')

def and16(a, b):
    "16-wide AND"
    return tuple(ai & bi for ai, bi in zip(a, b))


def test_or16():
    a = wires(16)
    b = wires(16)
    out = or16(a, b)
    simtest.test(locals(), 'tests/1/Or16.tst')

def or16(a, b):
    "16-wide OR"
    return tuple(ai | bi for ai, bi in zip(a, b))


def test_mux16():
    a = wires(16)
    b = wires(16)
    sel = Wire()
    out = mux16(a, b, sel)
    simtest.test(locals(), 'tests/1/Mux16.tst')

def mux16(a, b, sel):
    "16-wide 2-way MUX"
    return tuple(mux(ai, bi, sel) for ai, bi in zip(a, b))


def test_or8way():
    in_ = wires(8)
    out = or8way(in_)
    simtest.test(locals(), 'tests/1/Or8way.tst')

def or8way(in_):
    assert 8 == len(in_)
    w1 = [in_[i] | in_[i+1] for i in range(0, 8, 2)]
    w2 = [w1[i] | w1[i+1] for i in range(0, 4, 2)]
    return w2[0] | w2[1]


def test_mux4way16():
    a = wires(16)
    b = wires(16)
    c = wires(16)
    d = wires(16)
    sel = wires(2)
    out = mux4way16(a, b, c, d, sel)
    simtest.test(locals(), 'tests/1/Mux4way16.tst')

def mux4way16(a, b, c, d, sel):
    assert (16, 16, 16, 16) == (len(a), len(b), len(c), len(d))
    assert 2 == len(sel)
    return mux16(mux16(a, b, sel[1]),
                 mux16(c, d, sel[1]),
                 sel[0])


def test_mux8way16():
    a = wires(16)
    b = wires(16)
    c = wires(16)
    d = wires(16)
    e = wires(16)
    f = wires(16)
    g = wires(16)
    h = wires(16)
    sel = wires(3)
    out = mux8way16(a, b, c, d, e, f, g, h, sel)
    simtest.test(locals(), 'tests/1/Mux8way16.tst')

def mux8way16(a, b, c, d, e, f, g, h, sel):
    assert [16] * 8 == map(len, [a, b, c, d, e, f, g, h])
    assert 3 == len(sel)
    return mux16(mux4way16(a, b, c, d, sel[1:]),
                 mux4way16(e, f, g, h, sel[1:]),
                 sel[0])


def test_dmux4way():
    in_ = Wire()
    sel = wires(2)
    a, b, c, d = dmux4way(in_, sel)
    simtest.test(locals(), 'tests/1/DMux4way.tst')

def dmux4way(in_, sel):
    "if sel=00 then (in,0,0,0) else ... if sel=11 then (0,0,0,in)"
    assert 2 == len(sel)
    w0, w1 = dmux(in_, sel[0])
    return dmux(w0, sel[1]) + dmux(w1, sel[1])


def test_dmux8way():
    in_ = Wire()
    sel = wires(3)
    a, b, c, d, e, f, g, h = dmux8way(in_, sel)
    simtest.test(locals(), 'tests/1/DMux8way.tst')

def dmux8way(in_, sel):
    """if sel=000 then (in,0,0,0,0,0,0,0) else ...
       if sel=111 then (0,0,0,0,0,0,0,in)"""
    assert 3 == len(sel)
    w0, w1 = dmux(in_, sel[0])
    return dmux4way(w0, sel[1:]) + dmux4way(w1, sel[1:])


def main():
    for name, value in globals().items():
        if name.startswith('test'):
            print name
            value()

if __name__ == '__main__':
    main()
