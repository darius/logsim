# SPOILER WARNING! HERE ARE SOLUTIONS TO THE CHAPTER 3 PROBLEMS.
# DO NOT READ THIS IF YOU WANT TO SOLVE THEM FOR YOURSELF.

import arithmetic
import gates
import logsim
from logsim import lo, hi, Wire, wires, DFF, \
    DeferredWire, deferred_wires, resolve
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


def test_register():
    in_, load = wires(16), Wire()
    out = register(in_, load)
    simtest.test(locals(), 'tests/3/a/Register.tst')

def register(in_, load):
    "16-bit register."
    return tuple(bit(in_i, load) for in_i in in_)


def test_ram8():
    in_, load, address = wires(16), Wire(), wires(3)
    out = ram8(in_, load, address)
    simtest.test(locals(), 'tests/3/a/RAM8.tst')

def ram8(in_, load, address):
    "Memory of 8 registers, each 16-bit wide."
    registers = tuple(register(in_, load & select)
                      for select in gates.dmux8way(hi, address))
    return gates.mux8way16(*(registers + (address,)))


def test_ram64():
    in_, load, address = wires(16), Wire(), wires(6)
    out = ram64(in_, load, address)
    simtest.test(locals(), 'tests/3/a/RAM64.tst')

def ram64(in_, load, address):
    "Memory of 64 registers, each 16-bit wide."
    rams = tuple(ram8(in_, load & select, address[-3:])
                 for select in gates.dmux8way(hi, address[:3]))
    return gates.mux8way16(*(rams + (address[:3],)))


def test_PC():
    in_, load, inc, reset = wires(16), Wire(), Wire(), Wire()
    out = PC(in_, load, inc, reset)
    simtest.test(locals(), 'tests/3/a/PC.tst')

def PC(in_, load, inc, reset):
    "16-bit counter with load and reset controls."
    out_ = deferred_wires(16)
    choice1 = gates.mux16(out_, arithmetic.inc16(out_), inc)
    choice2 = gates.mux16(choice1, in_, load)
    choice3 = gates.mux16(choice2, (lo,) * 16, reset)
    return resolve(out_, register(choice3, hi))


if __name__ == '__main__':
    simtest.main(globals())
