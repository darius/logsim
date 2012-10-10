"""
A smoke test for sequential circuit simulation.
"""

from logsim import *

sim = Sim()

load = Wire()
inp = Wire()
out_ = DeferredWire()
#out = DFF(nand(nand(load, inp),
#               nand(nand(load, load), out_)))
a = nand(load, load)
b = nand(load, inp)
c = nand(a, out_)
d = nand(b, c)
out = DFF(d)
out_.resolve(out)

print 0, a.value, b.value, c.value, d.value, out.value, out_.value
sim.initialize(load, False)
sim.initialize(inp, False)
sim.ticktock(); print 1, a.value, b.value, c.value, d.value, out.value, out_.value
sim.initialize(load, True)
sim.ticktock(); print 2, a.value, b.value, c.value, d.value, out.value, out_.value
sim.initialize(load, False)
sim.ticktock(); print 3, a.value, b.value, c.value, d.value, out.value, out_.value
sim.initialize(load, True)
sim.initialize(inp, True)
sim.ticktock(); print 4, a.value, b.value, c.value, d.value, out.value, out_.value
sim.initialize(load, False)
sim.ticktock(); print 5, a.value, b.value, c.value, d.value, out.value, out_.value
sim.ticktock(); print 6, a.value, b.value, c.value, d.value, out.value, out_.value
