# SPOILER WARNING! HERE ARE SOLUTIONS TO THE CHAPTER 2 PROBLEMS.
# DO NOT READ THIS IF YOU WANT TO SOLVE THEM FOR YOURSELF.

import logsim
from logsim import Wire, wires
import simtest


def test_half_adder():
    a, b = wires(2)
    sum, carry = half_adder(a, b)
    simtest.test(locals(), 'tests/2/HalfAdder.tst')

def half_adder(a, b):
    "Compute the lsb and msb of a+b."
    return a ^ b, a & b


def test_full_adder():
    a, b, c = wires(3)
    sum, carry = full_adder(a, b, c)
    simtest.test(locals(), 'tests/2/FullAdder.tst')

def full_adder(a, b, c):
    "Compute the lsb and msb of a+b+c."
    s1, c1 = half_adder(a, b)
    s2, c2 = half_adder(s1, c)
    return s2, c1 | c2


def test_add16():
    a, b = wires(16), wires(16)
    # XXX these tuples are msb-first, how irritating
    out = rt(add16(rt(a), rt(b)))
    simtest.test(locals(), 'tests/2/Add16.tst')

def add16(a, b):
    "Compute a+b for 16-bit unsigned numbers."
    assert (16, 16) == (len(a), len(b))
    sum, carry = half_adder(a[0], b[0])
    out = [sum]
    for wa, wb in zip(a, b)[1:]:
        sum, carry = full_adder(wa, wb, carry)
        out.append(sum)
    assert 16 == len(out)
    for w in out:
        assert isinstance(w, logsim.Wire)
    return out


def rt(xs):
    return tuple(reversed(xs))


def test_inc16():
    in_ = wires(16)
    out = rt(inc16(rt(in_)))
    simtest.test(locals(), 'tests/2/Inc16.tst')

def inc16(in_):
    "Compute in_+1 for 16-bit unsigned numbers."
    assert 16 == len(in_)
    sum, carry = ~in_[0], in_[0]
    out = [sum]
    for w in in_[1:]:
        sum, carry = half_adder(w, carry)
        out.append(sum)
    return out


if __name__ == '__main__':
    simtest.main(globals())
