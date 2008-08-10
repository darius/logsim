from logsim import Wire
import simtest

def test_not():
    in_ = Wire()
    out = ~in_
    simtest.test(locals(), 'tests/1/Not.tst')

def test_and():
    a = Wire()
    b = Wire()
    out = a & b
    simtest.test(locals(), 'tests/1/And.tst')

def test_or():
    a = Wire()
    b = Wire()
    out = a | b
    simtest.test(locals(), 'tests/1/Or.tst')

def test_xor():
    a = Wire()
    b = Wire()
    out = a ^ b
    simtest.test(locals(), 'tests/1/Xor.tst')


def main():
    for name, value in globals().items():
        if name.startswith('test'):
            print name
            value()
    print 'All tests passed.'

if __name__ == '__main__':
    main()
