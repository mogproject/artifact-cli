# -*- encoding: utf-8 -*-

import unittest
from artifactcli.util.unicodeutil import *


class TestAssertType(unittest.TestCase):
    def test_unicode_char_width(self):
        self.assertEqual(unicode_char_width('x'), 1)
        self.assertEqual(unicode_char_width('あ'), 2)

    def test_unicode_char_width_error(self):
        self.assertRaises(TypeError, unicode_char_width, 'x'.encode())
        self.assertRaises(TypeError, unicode_char_width, 'あ'.encode())

    def test_unicode_width(self):
        self.assertEqual(unicode_width('x'), 1)
        self.assertEqual(unicode_width('あ'), 2)
        self.assertEqual(unicode_width('xあyいz'), 7)

    def test_unicode_width_error(self):
        self.assertRaises(TypeError, unicode_width, 123)

    def test_unicode_ljust(self):
        self.assertEqual(unicode_ljust('abc', 1), 'abc')
        self.assertEqual(unicode_ljust('abc', 3), 'abc')
        self.assertEqual(unicode_ljust('abc', 5), 'abc  ')
        self.assertEqual(unicode_ljust('あいう', -1), 'あいう')
        self.assertEqual(unicode_ljust('あいう', 1), 'あいう')
        self.assertEqual(unicode_ljust('あいう', 6), 'あいう')
        self.assertEqual(unicode_ljust('あいう', 10), 'あいう    ')
        self.assertEqual(unicode_ljust('あいう', 10, 'x'), 'あいうxxxx')
        self.assertEqual(unicode_ljust('あいう', 11, 'x'), 'あいうxxxxx')
        self.assertEqual(unicode_ljust('あいう', 10, 'あ'), 'あいうああ')
        self.assertEqual(unicode_ljust('あいう', 11, 'あ'), 'あいうああ')

    def test_unicode_ljust_error(self):
        self.assertRaises(TypeError, unicode_ljust, 'あいう', 10, '')
        self.assertRaises(TypeError, unicode_ljust, 'あいう', 10, 'xx')
        self.assertRaises(TypeError, unicode_ljust, 'あいう', 10, 'ああ')

    def test_unicode_rjust(self):
        self.assertEqual(unicode_rjust('abc', 1), 'abc')
        self.assertEqual(unicode_rjust('abc', 3), 'abc')
        self.assertEqual(unicode_rjust('abc', 5), '  abc')
        self.assertEqual(unicode_rjust('あいう', -1), 'あいう')
        self.assertEqual(unicode_rjust('あいう', 1), 'あいう')
        self.assertEqual(unicode_rjust('あいう', 6), 'あいう')
        self.assertEqual(unicode_rjust('あいう', 10), '    あいう')
        self.assertEqual(unicode_rjust('あいう', 10, 'x'), 'xxxxあいう')
        self.assertEqual(unicode_rjust('あいう', 11, 'x'), 'xxxxxあいう')
        self.assertEqual(unicode_rjust('あいう', 10, 'あ'), 'あああいう')
        self.assertEqual(unicode_rjust('あいう', 11, 'あ'), 'あああいう')

    def test_unicode_rjust_error(self):
        self.assertRaises(TypeError, unicode_rjust, 'あいう', 10, '')
        self.assertRaises(TypeError, unicode_rjust, 'あいう', 10, 'xx')
        self.assertRaises(TypeError, unicode_rjust, 'あいう', 10, 'ああ')

    def test_unicode_center(self):
        self.assertEqual(unicode_center('abc', 1), 'abc')
        self.assertEqual(unicode_center('abc', 3), 'abc')
        self.assertEqual(unicode_center('abc', 5), ' abc ')
        self.assertEqual(unicode_center('abc', 10), '   abc    ')
        self.assertEqual(unicode_center('あいう', -1), 'あいう')
        self.assertEqual(unicode_center('あいう', 1), 'あいう')
        self.assertEqual(unicode_center('あいう', 6), 'あいう')
        self.assertEqual(unicode_center('あいう', 7), 'あいう ')
        self.assertEqual(unicode_center('あいう', 10), '  あいう  ')
        self.assertEqual(unicode_center('あいう', 11), '  あいう   ')
        self.assertEqual(unicode_center('あいう', 12), '   あいう   ')
        self.assertEqual(unicode_center('あいう', 10, 'x'), 'xxあいうxx')
        self.assertEqual(unicode_center('あいう', 11, 'x'), 'xxあいうxxx')
        self.assertEqual(unicode_center('あいう', 10, 'あ'), 'ああいうあ')
        self.assertEqual(unicode_center('あいう', 11, 'あ'), 'ああいうあ')
        self.assertEqual(unicode_center('あいう', 12, 'あ'), 'ああいうああ')
        self.assertEqual(unicode_center('あいう', 13, 'あ'), 'ああいうああ')
        self.assertEqual(unicode_center('あいう', 14, 'あ'), 'あああいうああ')

    def test_unicode_center_error(self):
        self.assertRaises(TypeError, unicode_center, 'あいう', 10, '')
        self.assertRaises(TypeError, unicode_center, 'あいう', 10, 'xx')
        self.assertRaises(TypeError, unicode_center, 'あいう', 10, 'ああ')
