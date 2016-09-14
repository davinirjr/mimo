import unittest

from mimo.connection.input import Input


class TestInput(unittest.TestCase):
    def test_peek(self):
        connection = Input('a')

        self.assertRaises(IndexError, connection.peek)
        connection.entities.append(1)
        self.assertEqual(1, connection.peek())

    def test_pop(self):
        connection = Input('a')

        self.assertRaises(IndexError, connection.pop)
        connection.entities.extend((1, 2, 3))
        self.assertEqual(1, connection.pop())
        self.assertEqual([2, 3], list(connection.entities))

    def test_extend(self):
        connection = Input('a', 3)

        self.assertFalse(connection.extend((1, 2, 3, 4)))
        self.assertEqual([1, 2, 3, 4], list(connection.entities))


if __name__ == '__main__':
    unittest.main()
