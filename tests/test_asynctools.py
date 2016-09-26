import asyncio
import unittest

from mimo import arange, azip


class TestRange(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()

    def test_range(self):
        iterator = arange(10)

        future = self.loop.create_task(iterator.__anext__())
        self.loop.run_until_complete(future)
        self.assertEqual(0, future.result())

        future = self.loop.create_task(iterator.__anext__())
        self.loop.run_until_complete(future)
        self.assertEqual(1, future.result())

        future = self.loop.create_task(iterator.__anext__())
        self.loop.run_until_complete(future)
        self.assertEqual(2, future.result())

        future = self.loop.create_task(iterator.__anext__())
        self.loop.run_until_complete(future)
        self.assertEqual(3, future.result())

        future = self.loop.create_task(iterator.__anext__())
        self.loop.run_until_complete(future)
        self.assertEqual(4, future.result())

        future = self.loop.create_task(iterator.__anext__())
        self.loop.run_until_complete(future)
        self.assertEqual(5, future.result())

        future = self.loop.create_task(iterator.__anext__())
        self.loop.run_until_complete(future)
        self.assertEqual(6, future.result())

        future = self.loop.create_task(iterator.__anext__())
        self.loop.run_until_complete(future)
        self.assertEqual(7, future.result())

        future = self.loop.create_task(iterator.__anext__())
        self.loop.run_until_complete(future)
        self.assertEqual(8, future.result())

        future = self.loop.create_task(iterator.__anext__())
        self.loop.run_until_complete(future)
        self.assertEqual(9, future.result())

        future = self.loop.create_task(iterator.__anext__())
        self.assertRaises(StopAsyncIteration, self.loop.run_until_complete, future)

    def test_zip(self):
        iterator = azip(arange(5), arange(5, 10), arange(10, 15))

        future = self.loop.create_task(iterator.__anext__())
        self.loop.run_until_complete(future)
        self.assertEqual((0, 5, 10), future.result())

        future = self.loop.create_task(iterator.__anext__())
        self.loop.run_until_complete(future)
        self.assertEqual((1, 6, 11), future.result())

        future = self.loop.create_task(iterator.__anext__())
        self.loop.run_until_complete(future)
        self.assertEqual((2, 7, 12), future.result())

        future = self.loop.create_task(iterator.__anext__())
        self.loop.run_until_complete(future)
        self.assertEqual((3, 8, 13), future.result())

        future = self.loop.create_task(iterator.__anext__())
        self.loop.run_until_complete(future)
        self.assertEqual((4, 9, 14), future.result())

        future = self.loop.create_task(iterator.__anext__())
        self.assertRaises(StopAsyncIteration, self.loop.run_until_complete, future)


if __name__ == '__main__':
    unittest.main()
