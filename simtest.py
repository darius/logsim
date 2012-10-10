import os
import re
import sys

import logsim


def main(dictlike):
    "Use like simtest.main(globals()) to run all the tests in your module."
    for name, value in dictlike.items():
        if name.startswith('test'):
            print name
            value()


def test(env, filename):
    Tester(bowdlerize(env)).run(open(filename))

def bowdlerize(env):
    "Rename, e.g., 'in_' to 'in'."
    return dict((name.rstrip('_'), value)
                for name, value in env.items())

class Tester:

    def __init__(self, env):
        self.env = env
        self.sim = logsim.Sim()
        self.test_file = None
        self.output_specs = None
        self.ref_filename = None
        self.out = sys.stdout

    def run(self, file):
        self.test_file = file
        self.out = open('output.cmp', 'w')
        for line in file:
            line = re.sub(r'//.*', '', line)
            line = line.strip()
            if not line:
                continue
            self.run1(line)
        self.out.close()
        if self.ref_filename is not None:
            self.check()

    def check(self):
        if 0 == os.system('diff -u %s %s'
                          % (self.ref_filename, 'output.cmp')):
            os.unlink('output.cmp')

    def run1(self, line):
        line = re.sub(r'[,;]$', '', line)  # XXX might need this char
        words = line.split()
        if words[0] == 'load':
            pass
        elif words[0] == 'output-file':
            pass
        elif words[0] == 'compare-to':
            dirname = os.path.split(self.test_file.name)[0] # XXX
            self.ref_filename = os.path.join(dirname, words[1])
        elif words[0] == 'output-list':
            self.parse_output_list(words[1:])
        elif words[0] == 'set':
            self.parse_set(words[1], words[2])
        elif words[0] == 'eval':
            self.eval()
        elif words[0] == 'output':
            self.output()
        elif words[0] == 'tick':
            self.tick()
        elif words[0] == 'tock':
            self.tock()
        else:
            raise Exception('Syntax error', words)

    def parse_output_list(self, spec_strings):
        self.output_list(map(self.parse_output_spec, spec_strings))

    def parse_output_spec(self, spec_string):
        label, rest = spec_string.split('%')
        base = rest[0]
        assert base in 'BS', spec_string
        lpadding, width, rpadding = map(int, rest[1:].split('.'))
        if base == 'B':
            def format(value):
                return center(lpadding + width + rpadding, value)
        elif base == 'S':
            def format(value):
                s = str(value)
                return spaces(lpadding) + s + spaces(rpadding + (width - len(s)))
        return label, format

    def parse_set(self, label, literal):
        self.set(self.env[label], self.parse_literal(literal))

    def set(self, wire, value):
        if isinstance(wire, tuple):
            for w, v in tupleize(wire, value):
                self.set(w, v)
        else:
            self.sim.set(wire, value)

    def parse_literal(self, literal):
        if literal.startswith('%B'):
            return int(literal[2:], 2)
        return int(literal)

    def output_list(self, specs):
        self.output_specs = specs
        write_list(self.out, specs)

    def eval(self):
        self.sim.ticktock()

    def tick(self):
        self.sim.tick()

    def tock(self):
        self.sim.tock()

    def output(self):
        self.env['time'] = FakeWire(self.sim.get_time())
        x = [(var_value(self.env[label]), format)
             for (label, format) in self.output_specs]
        write_list(self.out, x)

class FakeWire:
    def __init__(self, value):
        self.value = value

def var_value(v):
    if isinstance(v, tuple):
        return tuple(map(var_value, v))
    if v.value == '?': return '0'  # XXX hack to make DFF outputs conform to the book
    return v.value

def tupleize(wires, value):
    assert isinstance(value, int)
    out = []
    for w in wires:
        out.append((w, value & 1))
        value >>= 1
    return out

def write_list(out, specs):
    out.write('|')
    for value, format in specs:
        out.write('%s|' % format(to_string(value)))
    out.write('\r\n')

def to_string(value):
    if isinstance(value, str):
        return value
    elif isinstance(value, bool):
        return str(int(value))
    elif isinstance(value, int):
        return base2(value)
    elif isinstance(value, tuple):
        return ''.join(reversed(map(to_string, value)))
    else:
        raise Exception('wtf?', value)

def base2(n):
    assert 0 <= n
    digit = str(n % 2)
    return digit if n < 2 else base2(n // 2) + digit

def spaces(n):
    return ' ' * n

def center(width, s):
    k = (width - len(s)) // 2
    return '%s%-*s' % (spaces(k), width - k, s)
