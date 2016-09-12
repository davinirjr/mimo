import unittest

from mimo.connection import Connection
from mimo.stream import Stream


class TestConnection(unittest.TestCase):
    def test_peek(self):
        connection = Connection('a')

        self.assertRaises(IndexError, connection.peek)
        connection.entities.append(1)
        self.assertEqual(1, connection.peek())

    def test_pop(self):
        connection = Connection('a')

        self.assertRaises(IndexError, connection.pop)
        connection.entities.extend((1, 2, 3))
        self.assertEqual(1, connection.pop())
        self.assertEqual([2, 3], list(connection.entities))

    def test_push(self):
        connection = Connection('a', 3)

        self.assertTrue(connection.push(1))
        self.assertEqual([1], list(connection.entities))
        self.assertTrue(connection.push(2))
        self.assertEqual([1, 2], list(connection.entities))
        self.assertFalse(connection.push(3))
        self.assertEqual([1, 2, 3], list(connection.entities))

    def test_extend(self):
        connection = Connection('a', 3)

        self.assertFalse(connection.extend((1, 2, 3, 4)))
        self.assertEqual([1, 2, 3, 4], list(connection.entities))

    def test_connect_to_input(self):
        connection = Connection('a')
        stream = Stream(['input'], ['output'])

        connection.join(stream, 'input')

        self.assertEqual(stream, next(iter(connection.streams)))
        self.assertEqual(stream.ins['input'], next(iter(connection.connections)))

    def test_drain(self):
        connection = Connection('a')
        stream = Stream(['input', 'output'])

        connection.join(stream, 'input')
        connection.entities.extend([1, 2, 3, 4, 5])
        connection.drain()

        self.assertEqual([1, 2, 3, 4, 5], list(stream.ins.input.entities))


if __name__ == '__main__':
    unittest.main()
