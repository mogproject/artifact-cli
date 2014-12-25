# -*- encoding: utf-8 -*-

import unittest
from artifactcli.util.unicodeutil import *


class TestAssertType(unittest.TestCase):
    def test_to_str(self):
        self.assertEqual(to_str('abc'), 'abc')
        self.assertEqual(to_str(u'abc'), 'abc')
        self.assertEqual(to_str('あいう'), 'あいう')
        self.assertEqual(to_str(u'あいう'), 'あいう')

    def test_to_str_error(self):
        self.assertRaises(ValueError, to_str, 123)

    def test_to_unicode(self):
        self.assertEqual(to_unicode('abc'), u'abc')
        self.assertEqual(to_unicode(u'abc'), u'abc')
        self.assertEqual(to_unicode('あいう'), u'あいう')
        self.assertEqual(to_unicode(u'あいう'), u'あいう')

    def test_to_unicode_error(self):
        self.assertRaises(ValueError, to_unicode, 123)

    def test_unicode_char_width(self):
        self.assertEqual(unicode_char_width(u'x'), 1)
        self.assertEqual(unicode_char_width(u'あ'), 2)

    def test_unicode_char_width_error(self):
        self.assertRaises(TypeError, unicode_char_width, 'x')
        self.assertRaises(TypeError, unicode_char_width, 'あ')

    def test_unicode_width(self):
        self.assertEqual(unicode_width(u'x'), 1)
        self.assertEqual(unicode_width(u'あ'), 2)
        self.assertEqual(unicode_width('x'), 1)
        self.assertEqual(unicode_width('あ'), 2)
        self.assertEqual(unicode_width(u'xあyいz'), 7)
        self.assertEqual(unicode_width('xあyいz'), 7)

    def test_unicode_width_error(self):
        self.assertRaises(ValueError, unicode_width, 123)

    def test_unicode_ljust(self):
        self.assertEqual(unicode_ljust('abc', 5), u'abc  ')
        self.assertEqual(unicode_ljust('abc', 3), u'abc')
        self.assertEqual(unicode_ljust('abc', 1), u'abc')
        self.assertEqual(unicode_ljust(u'abc', 5), u'abc  ')
        self.assertEqual(unicode_ljust(u'abc', 3), u'abc')
        self.assertEqual(unicode_ljust(u'abc', 1), u'abc')
        self.assertEqual(unicode_ljust('あいう', 10), u'あいう    ')
        self.assertEqual(unicode_ljust('あいう', 6), u'あいう')
        self.assertEqual(unicode_ljust('あいう', 1), u'あいう')
        self.assertEqual(unicode_ljust('あいう', -1), u'あいう')
        self.assertEqual(unicode_ljust(u'あいう', 10), u'あいう    ')
        self.assertEqual(unicode_ljust(u'あいう', 6), u'あいう')
        self.assertEqual(unicode_ljust(u'あいう', 1), u'あいう')
        self.assertEqual(unicode_ljust('あいう', 10, 'x'), u'あいうxxxx')
        self.assertEqual(unicode_ljust(u'あいう', 10, 'x'), u'あいうxxxx')
        self.assertEqual(unicode_ljust(u'あいう', 11, 'x'), u'あいうxxxxx')
        self.assertEqual(unicode_ljust(u'あいう', 10, u'あ'), u'あいうああ')
        self.assertEqual(unicode_ljust(u'あいう', 11, u'あ'), u'あいうああ')

    def test_unicode_ljust_error(self):
        self.assertRaises(TypeError, unicode_ljust, u'あいう', 10, '')
        self.assertRaises(TypeError, unicode_ljust, u'あいう', 10, u'')
        self.assertRaises(TypeError, unicode_ljust, u'あいう', 10, 'xx')
        self.assertRaises(TypeError, unicode_ljust, u'あいう', 10, 'あ')
        self.assertRaises(TypeError, unicode_ljust, u'あいう', 10, u'ああ')

    def test_unicode_rjust(self):
        self.assertEqual(unicode_rjust('abc', 5), u'  abc')
        self.assertEqual(unicode_rjust('abc', 3), u'abc')
        self.assertEqual(unicode_rjust('abc', 1), u'abc')
        self.assertEqual(unicode_rjust(u'abc', 5), u'  abc')
        self.assertEqual(unicode_rjust(u'abc', 3), u'abc')
        self.assertEqual(unicode_rjust(u'abc', 1), u'abc')
        self.assertEqual(unicode_rjust('あいう', 10), u'    あいう')
        self.assertEqual(unicode_rjust('あいう', 6), u'あいう')
        self.assertEqual(unicode_rjust('あいう', 1), u'あいう')
        self.assertEqual(unicode_rjust('あいう', -1), u'あいう')
        self.assertEqual(unicode_rjust(u'あいう', 10), u'    あいう')
        self.assertEqual(unicode_rjust(u'あいう', 6), u'あいう')
        self.assertEqual(unicode_rjust(u'あいう', 1), u'あいう')
        self.assertEqual(unicode_rjust('あいう', 10, 'x'), u'xxxxあいう')
        self.assertEqual(unicode_rjust(u'あいう', 10, 'x'), u'xxxxあいう')
        self.assertEqual(unicode_rjust(u'あいう', 11, 'x'), u'xxxxxあいう')
        self.assertEqual(unicode_rjust(u'あいう', 10, u'あ'), u'あああいう')
        self.assertEqual(unicode_rjust(u'あいう', 11, u'あ'), u'あああいう')

    def test_unicode_rjust_error(self):
        self.assertRaises(TypeError, unicode_rjust, u'あいう', 10, '')
        self.assertRaises(TypeError, unicode_rjust, u'あいう', 10, u'')
        self.assertRaises(TypeError, unicode_rjust, u'あいう', 10, 'xx')
        self.assertRaises(TypeError, unicode_rjust, u'あいう', 10, 'あ')
        self.assertRaises(TypeError, unicode_rjust, u'あいう', 10, u'ああ')

    def test_unicode_center(self):
        self.assertEqual(unicode_center('abc', 5), u' abc ')
        self.assertEqual(unicode_center('abc', 10), u'   abc    ')
        self.assertEqual(unicode_center('abc', 3), u'abc')
        self.assertEqual(unicode_center('abc', 1), u'abc')
        self.assertEqual(unicode_center(u'abc', 5), u' abc ')
        self.assertEqual(unicode_center(u'abc', 3), u'abc')
        self.assertEqual(unicode_center(u'abc', 1), u'abc')
        self.assertEqual(unicode_center('あいう', 10), u'  あいう  ')
        self.assertEqual(unicode_center('あいう', 6), u'あいう')
        self.assertEqual(unicode_center('あいう', 1), u'あいう')
        self.assertEqual(unicode_center('あいう', -1), u'あいう')
        self.assertEqual(unicode_center(u'あいう', 10), u'  あいう  ')
        self.assertEqual(unicode_center(u'あいう', 11), u'  あいう   ')
        self.assertEqual(unicode_center(u'あいう', 12), u'   あいう   ')
        self.assertEqual(unicode_center(u'あいう', 7), u'あいう ')
        self.assertEqual(unicode_center(u'あいう', 6), u'あいう')
        self.assertEqual(unicode_center(u'あいう', 1), u'あいう')
        self.assertEqual(unicode_center('あいう', 10, 'x'), u'xxあいうxx')
        self.assertEqual(unicode_center(u'あいう', 10, 'x'), u'xxあいうxx')
        self.assertEqual(unicode_center(u'あいう', 11, 'x'), u'xxあいうxxx')
        self.assertEqual(unicode_center(u'あいう', 10, u'あ'), u'ああいうあ')
        self.assertEqual(unicode_center(u'あいう', 11, u'あ'), u'ああいうあ')
        self.assertEqual(unicode_center(u'あいう', 12, u'あ'), u'ああいうああ')
        self.assertEqual(unicode_center(u'あいう', 13, u'あ'), u'ああいうああ')
        self.assertEqual(unicode_center(u'あいう', 14, u'あ'), u'あああいうああ')

    def test_unicode_center_error(self):
        self.assertRaises(TypeError, unicode_center, u'あいう', 10, '')
        self.assertRaises(TypeError, unicode_center, u'あいう', 10, u'')
        self.assertRaises(TypeError, unicode_center, u'あいう', 10, 'xx')
        self.assertRaises(TypeError, unicode_center, u'あいう', 10, 'あ')
        self.assertRaises(TypeError, unicode_center, u'あいう', 10, u'ああ')
