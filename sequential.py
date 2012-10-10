# SPOILER WARNING! HERE ARE SOLUTIONS TO THE CHAPTER 3 PROBLEMS.
# DO NOT READ THIS IF YOU WANT TO SOLVE THEM FOR YOURSELF.

import gates
import logsim
from logsim import Wire, DeferredWire, wires, DFF
import simtest


def test_bit():
    in_, load = wires(2)
    out = bit(in_, load)
    simtest.test(locals(), 'tests/3/a/Bit.tst')

def bit(in_, load):
    "1-bit register."
    out_ = DeferredWire()
    out = DFF(gates.mux(out_, in_, load))
    out_.resolve(out)
    return out


if __name__ == '__main__':
    simtest.main(globals())
