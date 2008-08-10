# SPOILER WARNING! HERE ARE SOLUTIONS TO THE CHAPTER 1 PROBLEMS.
# DO NOT READ THIS IF YOU WANT TO SOLVE THEM FOR YOURSELF.

from logsim import Wire, nand
import simtest

def not_(a):
    return nand(a, a)

def test_not():
    in_ = Wire()
    out = ~in_
    simtest.test(locals(), 'tests/1/Not.tst')

def and_(a, b):
    return ~nand(a, b)

def test_and():
    a = Wire()
    b = Wire()
    out = a & b
    simtest.test(locals(), 'tests/1/And.tst')

def or_(a, b):
    return nand(~a, ~b)

def test_or():
    a = Wire()
    b = Wire()
    out = a | b
    simtest.test(locals(), 'tests/1/Or.tst')

def xor(a, b):
    return nand(nand(a, ~b),
                nand(~a, b))

def test_xor():
    a = Wire()
    b = Wire()
    out = a ^ b
    simtest.test(locals(), 'tests/1/Xor.tst')


def main():
    for name, value in globals().items():
        if name.startswith('test'):
            print name
            value()
    print 'All tests passed.'

if __name__ == '__main__':
    main()
