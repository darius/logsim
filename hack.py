# SPOILER WARNING! HERE ARE SOLUTIONS TO THE CHAPTER 5 PROBLEMS.
# DO NOT READ THIS IF YOU WANT TO SOLVE THEM FOR YOURSELF.

import logsim
from logsim import lo, hi, Wire, wires, DFF, \
    DeferredWire, deferred_wires, resolve
import simtest

from arithmetic import alu
from gates import mux16
from sequential import register, PC

def test_CPU():
    inM, instruction, reset = wires(16), wires(16), Wire()
    outM, writeM, addressM, pc = CPU(inM, instruction, reset)
    simtest.test(locals(), 'tests/5/CPU.tst')

def CPU(inM, instruction, reset, sim=None):
    """The Central Processing unit (CPU). Inputs:
      * inM from data memory
      * instruction from program memory
      * reset to restart from address 0.
    Outputs:
      * outM, writeM, addressM to data memory (for an instruction
        writing to M).
      * pc addressing program memory to fetch the next instruction.
    """
    j3, j2, j1 = instruction[0:3]
    d3, d2, d1 = instruction[3:6]
    c6, c5, c4, c3, c2, c1 = instruction[6:12]
    a_bit = instruction[12]
    c_insn = instruction[15] & instruction[14] & instruction[13]

    outM = deferred_wires(16)

    a_mux = mux16(instruction, outM, c_insn)
    a_reg = register(a_mux, ~instruction[15] | (c_insn & d1))
    d_reg = register(outM, d2 & c_insn)
    
    if sim:
        sim.watch(a_mux, 'a_mux')
        sim.watch(a_reg, 'A')

    writeM = c_insn & d3

    addressM = a_reg

    y_mux = mux16(a_reg, inM, a_bit)
    # XXX double-check alu x/y inputs
    alu_out, alu_zr, alu_ng = alu(x=d_reg, y=y_mux,
                                  zx=c1, nx=c2, zy=c3, ny=c4, f=c5, no=c6)
    resolve(outM, alu_out)

    pcinc = ~(j1 & alu_ng | j2 & alu_zr | j3 & ~alu_zr & ~alu_ng)
    pc = PC(a_reg, ~pcinc, pcinc, reset)

    return outM, writeM, addressM, pc


def my_test():
    sim = logsim.Sim()
    def setv(wires, value):
        for i, w in enumerate(wires):
            sim.initialize(w, (value >> i) & 1)

    inM, instruction, reset = wires(16), wires(16), Wire()
    outM, writeM, addressM, pc = CPU(inM, instruction, reset, sim)

    sim.watch(instruction, 'instruction')
    sim.watch(outM, 'outM')
    sim.watch(writeM, 'writeM')
    sim.watch(addressM, 'addressM')
    sim.watch(pc, 'pc')

    sim.initialize(reset, 1)
    setv(inM, 0)
    setv(instruction, 0)
    sim.tick(); sim.tock()

    sim.time = 0

    sim.initialize(reset, 0)
    setv(instruction, int('0011000000111001', 2))
    sim.tick(); sim.tock()

    sim.tick(); sim.tock()


if __name__ == '__main__':
    simtest.main(globals())
    my_test()
