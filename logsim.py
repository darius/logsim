def initialize(entries):
    "Helper for __init__ methods."
    entries['self'].__dict__.update((key, value) 
                                    for key, value in entries.items()
                                    if key != 'self')


class Sim:
    def __init__(self):
        self.pending = {}
        self.true = Wire()
        self.set(self.true, True)
        self.false = Wire()
        self.set(self.false, False)
    def set(self, wire, value):
        wire.value = '?'
        self.pending[wire] = value
        # XXX detect conflicting writes (races)
    def run(self):
        while self.pending:
            self.pending = step(self.pending)

def step(pending):
    dirty = set()
    for w, new_value in pending.items():
        if w.value != new_value:
            w.value = new_value
            for gate in w.readers:
                dirty.add(gate)
    new_pending = {}
    for gate in dirty:
        gate.run(new_pending)
    return new_pending

class Wire:
    def __init__(self):
        self.readers = []
        self.value = '?'
    def add_reader(self, gate):
        if gate not in self.readers:
            self.readers.append(gate)
    def __invert__(self):
        import gates
        return gates.not_(self)
    def __and__(self, other):
        import gates
        return gates.and_(self, other)
    def __or__(self, other):
        import gates
        return gates.or_(self, other)
    def __xor__(self, other):
        import gates
        return gates.xor(self, other)

# XXX Currently if you use these, you must make sure to connect them
# to gates that will be scheduled for update by other wires. Ugh ugh ugh.
true = Wire()
true.value = True
false = Wire()
false.value = False

class Nand:
    def __init__(self, in1, in2, out):
        initialize(locals())
        in1.add_reader(self)
        in2.add_reader(self)
    def run(self, pending):
        pending[self.out] = not (self.in1.value and self.in2.value)

def nand(in1, in2):
    out = Wire()
    Nand(in1, in2, out)
    return out
