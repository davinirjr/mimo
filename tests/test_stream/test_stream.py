import unittest

from mimo import Stream
from mimo.connection.connection_set import ConnectionSet
from mimo.connection.input import Input
from mimo.connection.output import Output


class TestStream(unittest.TestCase):
    def test_run(self):
        stream = Stream(['a'], ['b'], fn=fn)
        input = Input('a', 5)
        ins = ConnectionSet([input])
        output = Output('b', 5)
        outs = ConnectionSet([output])
        input.entities.extend([1, 2, 3, 4, 5, 6, 7, 8, 9, 0])

        self.assertTrue(stream.run(ins, outs))
        self.assertEqual([2, 4, 6, 8, 10], list(output.entities))
        self.assertTrue(stream.run(ins, outs))
        self.assertEqual([2, 4, 6, 8, 10, 12], list(output.entities))
        output.entities.clear()
        self.assertFalse(stream.run(ins, outs))
        self.assertEqual([14, 16, 18, 0], list(output.entities))


def fn(ins, outs, state):
    while len(ins.a) > 0:
        if not outs.b.push(2 * ins.a.pop()):
            return True


if __name__ == '__main__':
    unittest.main()
