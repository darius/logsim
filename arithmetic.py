# SPOILER WARNING! HERE ARE SOLUTIONS TO THE CHAPTER 2 PROBLEMS.
# DO NOT READ THIS IF YOU WANT TO SOLVE THEM FOR YOURSELF.

import logsim
from logsim import Wire, nand, false, wires
import simtest


def test_half_adder():
    a = Wire()
    b = Wire()
    sum, carry = half_adder(a, b)
    simtest.test(locals(), 'tests/2/HalfAdder.tst')

def half_adder(a, b):
    "Compute the lsb and msb of a+b."
    return a ^ b, a & b



if __name__ == '__main__':
    simtest.main(globals())
