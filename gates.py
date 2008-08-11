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


def main():
    for name, value in globals().items():
        if name.startswith('test'):
            print name
            value()

if __name__ == '__main__':
    main()
