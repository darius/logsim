"""
Tabulate all possible inputs to a combinational circuit, together
with its output in each case.
"""

from itertools import product

import logsim

def tabulate(in_wires, out_wires):
    sim = logsim.Sim()
    for values in truth_table(in_wires):
        for wire, value in zip(in_wires, values):
            sim.initialize(wire, value)
        sim.ticktock()
        print ' '.join(map(str, wire_values(in_wires) + wire_values(out_wires)))

def wire_values(wires):
    return [wire.value for wire in wires]

def truth_table(wires):
    return product(*[(0, 1)]*len(wires))


if True:
    a = logsim.Wire()
    b = logsim.Wire()
    tabulate([a, b], [logsim.nand(a, b)])
    print ''
    tabulate([a, b], [a & b])
    print ''
    tabulate([a, b], [a | b])
    print ''
    tabulate([a, b], [a ^ b])
    print ''
