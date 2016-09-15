import unittest

from mimo.connection.output import Output


class TestOutput(unittest.TestCase):
    def test_push(self):
        connection = Output('a', 3)

        self.assertTrue(connection.push(1))
        self.assertEqual([1], list(connection.entities))
        self.assertTrue(connection.push(2))
        self.assertEqual([1, 2], list(connection.entities))
        self.assertFalse(connection.push(3))
        self.assertEqual([1, 2, 3], list(connection.entities))


if __name__ == '__main__':
    unittest.main()
