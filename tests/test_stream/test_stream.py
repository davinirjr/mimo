import unittest

from mimo import Stream
from mimo.test_helper import TestHelper


class TestStream(unittest.TestCase):
    def test_run(self):
        stream = Stream(['a'], ['b'], fn=fn)
        helper = TestHelper(stream)

        self.assertEqual({'b': [2, 4, 6, 8, 10, 12, 14, 16, 18, 0]}, helper.run({'a': [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]}))


async def fn(ins, outs, state):
    async for item in ins.a:
        await outs.b.push(2 * item)


if __name__ == '__main__':
    unittest.main()
