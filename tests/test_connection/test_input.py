import asyncio
import unittest

from mimo.connection.input import Input, ConnectionClosed


class TestInput(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()

    def test_push(self):
        connection = Input('a')

        self.loop.run_until_complete(connection.push(0))

        self.assertIn(0, connection._queue)

    def test_push_closed(self):
        connection = Input('a')
        connection.close()

        task = self.loop.create_task(connection.push(0))

        self.assertRaises(ConnectionClosed, self.loop.run_until_complete, task)

    def test_peek(self):
        connection = Input('a')
        connection._queue.extend((0, 1, 2))

        task = self.loop.create_task(connection.peek())
        self.loop.run_until_complete(task)

        self.assertEqual(0, task.result())
        self.assertEqual([0, 1, 2], list(connection._queue))

    def test_pop(self):
        connection = Input('a')
        connection._queue.extend((0, 1, 2))

        task = self.loop.create_task(connection.pop())
        self.loop.run_until_complete(task)

        self.assertEqual(0, task.result())
        self.assertEqual([1, 2], list(connection._queue))


if __name__ == '__main__':
    unittest.main()
