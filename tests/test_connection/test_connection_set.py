import unittest

from mimo.connection.output import Output
from mimo.connection.connection_set import ConnectionSet


class TestConnectionSet(unittest.TestCase):
    def test_items_and_attributes(self):
        a = Output('a')
        b = Output('b')
        connection_set = ConnectionSet([a, b])

        self.assertEqual(a, connection_set.a)
        self.assertEqual(b, connection_set.b)
        self.assertEqual(a, connection_set['a'])
        self.assertEqual(b, connection_set['b'])


if __name__ == '__main__':
    unittest.main()
