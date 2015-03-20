"""
Some exhaustive tests.
TODO: check add16 using a BDD
"""

import arithmetic as A
import logsim as S
from tabulate import truth_table, wire_values

def test_half_adder():
    exhaustive_test(half_adder, A.half_adder, 2)

def half_adder(a, b):
    sum2 = a + b
    carry, sum = sum2>>1, sum2&1
    return sum, carry

def test_full_adder():
    exhaustive_test(full_adder, A.full_adder, 3)

def full_adder(a, b, c):
    sum2 = a + b + c
    carry, sum = sum2>>1, sum2&1
    return sum, carry

def test_inc16():
    exhaustive_test(inc16, lambda *in_: A.inc16(in_), 16)

def inc16(*in_):
    n = sum((1<<i) for i, bit in enumerate(in_) if bit)
    result = n+1
    return tuple((result>>i)&1 for i in range(len(in_)))

def exhaustive_test(spec, builder, ninputs):
    inputs = S.wires(ninputs)
    outputs = builder(*inputs)
    for values in truth_table('x'*ninputs):
        #print values, 'spec', spec(*values), 'circuit', run(inputs, values, outputs)
        assert spec(*values) == run(values, outputs, inputs)

def run(values, outputs, inputs):
    sim = S.Sim()
    for wire, value in zip(inputs, values):
        sim.initialize(wire, value)
    sim.ticktock()
    return tuple(wire_values(outputs))

## test_half_adder()
## test_full_adder()
# test_inc16()


if __name__ == '__main__':
    test_half_adder()
    test_full_adder()
    test_inc16()
    #test_add16()
