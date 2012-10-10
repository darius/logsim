def power_up():
    agenda.clear()
    initialize(lo, 0)
    initialize(hi, 1)

agenda = {}

def initialize(wire, value):
    wire.value = '?'
    agenda[wire] = value

def ticktock():
    global agenda
    fine_agenda = agenda
    coarse_agenda = {}
    while fine_agenda:
        dirty = set().union(*[wire(new_value) for wire, new_value in fine_agenda.items()])
        new_agenda = {}
        for gate in dirty:
            gate(new_agenda, coarse_agenda)
        fine_agenda = new_agenda
    agenda = coarse_agenda

def Wire():
    def wire(new_value):
        if wire.value == new_value: return set()
        wire.value = new_value
        return readers
    readers = set()
    wire.acquaint = readers.add
    wire.value = '?'
    return wire

def DeferredWire():
    def wire(new_value):
        assert False, "You directly set a deferred wire."
    def set_me(new_value):
        wire.value = new_value
        return readers
    def resolve(resolution):
        assert not resolve.resolved; resolve.resolved = True
        def propagate(agenda, coarse_agenda):
            agenda[set_me] = resolution.value
        resolution.acquaint(propagate)
    resolve.resolved = False
    wire.resolve = resolve
    readers = set()
    wire.acquaint = readers.add
    wire.value = '?'
    return wire

lo, hi = Wire(), Wire()

def nand(in1, in2):
    out = Wire()
    def propagate(agenda, coarse_agenda):
        # nand(a, b) is just (not (a and b)), but an input may be
        # undetermined ('?'). Also the output is sometimes determined
        # even given one '?' input (when the other is 0).
        agenda[out] = (1 if not in1.value or not in2.value
                       else '?' if '?' in (in1.value, in2.value)
                       else 0)
    in1.acquaint(propagate)
    in2.acquaint(propagate)
    return out

def DFF(in_):
    out = Wire()
    def propagate(agenda, coarse_agenda):
        coarse_agenda[out] = in_.value # XXX
    in_.acquaint(propagate)
    return out


##############################################################

if False:

    a = Wire()
    feedback = DeferredWire()
    b = nand(a, feedback)
    c = DFF(b)
    feedback.resolve(c)

    power_up(); print 0, c.value
    initialize(a, 0)
    ticktock(); print 1, c.value
    initialize(a, 1)
    ticktock(); print 2, c.value
    initialize(a, 0)
    ticktock(); print 3, c.value
    initialize(a, 1)
    ticktock(); print 4, c.value

if False:
    a = Wire()
    b = nand(a, a)
    power_up(); print 0, a.value, b.value
    initialize(a, True)
    ticktock(); print 1, a.value, b.value
    print

load = Wire()
inp = Wire()
a = nand(load, inp)
power_up(); print 0, a.value
initialize(load, 0)
initialize(inp, 0)
ticktock(); print 1, a.value
initialize(load, 1)
ticktock(); print 2, a.value
print


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

power_up(); print 0, a.value, b.value, c.value, d.value, out.value, out_.value
initialize(load, False)
initialize(inp, False)
ticktock(); print 1, a.value, b.value, c.value, d.value, out.value, out_.value
initialize(load, True)
ticktock(); print 2, a.value, b.value, c.value, d.value, out.value, out_.value
initialize(load, False)
ticktock(); print 3, a.value, b.value, c.value, d.value, out.value, out_.value
initialize(load, True)
initialize(inp, True)
ticktock(); print 4, a.value, b.value, c.value, d.value, out.value, out_.value
initialize(load, False)
ticktock(); print 5, a.value, b.value, c.value, d.value, out.value, out_.value
ticktock(); print 6, a.value, b.value, c.value, d.value, out.value, out_.value

