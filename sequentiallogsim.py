"""
Basic components of a circuit, and simulating their behavior.
"""

class Sim:

    def __init__(self):
        self.agenda = {}
        self.lo, self.hi = Wire(), Wire()
        self.power_up()

    def power_up(self):
        self.agenda.clear()
        self.initialize(self.lo, 0)
        self.initialize(self.hi, 1)

    def initialize(self, wire, value):
        wire.value = '?'
        self.agenda[wire] = value

    def ticktock(self):
        fine_agenda = self.agenda
        coarse_agenda = {}
        while fine_agenda:
            dirty = set().union(*[wire(new_value) for wire, new_value in fine_agenda.items()])
            new_agenda = {}
            for gate in dirty:
                gate(new_agenda, coarse_agenda)
            fine_agenda = new_agenda
        self.agenda = coarse_agenda

class Wire:

    def __init__(self):
        self.value = '?'
        self.readers = set()

    def __call__(self, new_value):
        if self.value == new_value: return set()
        self.value = new_value
        return self.readers

    def acquaint(self, reader):
        self.readers.add(reader)

class DeferredWire(Wire):

    def __init__(self):
        Wire.__init__(self)
        self.wire = None

    def __call__(self, new_value):
        assert False, "You directly set a deferred wire."

    def resolve(self, resolution):
        assert self.wire is None, "DeferredWire already resolved"
        self.wire = resolution
        resolution.acquaint(self._propagate)

    def _propagate(self, agenda, coarse_agenda):
        agenda[self._set_me] = self.wire.value

    def _set_me(self, new_value):
        self.value = new_value
        return self.readers

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
        coarse_agenda[out] = in_.value # XXX test me more
    in_.acquaint(propagate)
    return out
