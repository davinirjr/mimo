import unittest

from mimo.connection import Connection, ConnectionSet


class TestConnectionSet(unittest.TestCase):
    def test_items_and_attributes(self):
        a = Connection('a')
        b = Connection('b')
        connections = ConnectionSet([a, b])

        self.assertEqual(a, connections.a)
        self.assertEqual(b, connections.b)
        self.assertEqual(a, connections['a'])
        self.assertEqual(b, connections['b'])

    def test_drain(self):
        connection = Connection('a')
        connection.entities.extend((1, 2, 3, 4))

        self.assertTrue(connection.drain())

    def test_drain_empty(self):
        connection = Connection('a')

        self.assertFalse(connection.drain())


if __name__ == '__main__':
    unittest.main()
