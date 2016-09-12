import unittest

from mimo import Stream


class TestStream(unittest.TestCase):
    def test_pipe(self):
        stream1 = Stream(['a'], ['b'])
        stream2 = Stream(['c'], ['d'])

        stream1.pipe(stream2)

        self.assertEqual({stream2}, stream1.children['b'])
        self.assertEqual({stream2.ins['c']}, stream1.outs['b'].connections)


if __name__ == '__main__':
    unittest.main()
