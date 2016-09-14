import unittest

from mimo.connection.connection import Connection


class TestConnection(unittest.TestCase):
    def test_is_full(self):
        connection = Connection('a', 5)

        self.assertFalse(connection.is_full())
        connection.entities.extend([1, 2, 3, 4, 5])
        self.assertTrue(connection.is_full())


if __name__ == '__main__':
    unittest.main()
