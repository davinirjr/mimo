import asyncio
import unittest

from mimo import Stream
from mimo.test_helper import TestHelper


class TestTestHelper(unittest.TestCase):
    def test_run(self):
        stream = Stream(ins=['a'], outs=['b'], fn=fn)
        helper = TestHelper(stream)

        self.assertEqual({'b': [2, 4, 6, 8, 10, 12, 14, 16, 18, 0]},
                         helper.run({'a': [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]}))

    def test_run_timeout(self):
        stream = Stream(ins=['a'], outs=['b'], fn=will_timeout)
        helper = TestHelper(stream, timeout=1)

        self.assertRaises(asyncio.TimeoutError, helper.run)


async def fn(ins, outs, state):
    async for item in ins.a:
        await outs.b.push(2 * item)


async def will_timeout(ins, outs, state):
    await asyncio.sleep(10)


if __name__ == '__main__':
    unittest.main()
