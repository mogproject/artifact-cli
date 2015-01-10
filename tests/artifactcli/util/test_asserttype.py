import unittest
from artifactcli.util.asserttype import assert_type


class TestAssertType(unittest.TestCase):
    def test_assert_type(self):
        self.assertEqual(assert_type(123, int), 123)
        self.assertEqual(assert_type('abc', str), 'abc')

    def test_assert_type_error(self):
        self.assertRaises(TypeError, assert_type, 123, str)
        self.assertRaises(TypeError, assert_type, 'abc', int)
