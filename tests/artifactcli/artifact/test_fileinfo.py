import unittest
from datetime import datetime
from artifactcli.artifact import FileInfo


class TestFileInfo(unittest.TestCase):
    def setUp(self):
        self.test_data = [
            FileInfo('HOST', 'USER', 0, datetime(2014, 12, 31, 12, 34, 56), '0'),
            FileInfo('HOST', 'USER', 10000000000000000000000000000, datetime(2014, 12, 31, 12, 34, 56), 'ffff'),
        ]

    def test_eq(self):
        self.assertTrue(self.test_data[0] == FileInfo('HOST', 'USER', 0, datetime(2014, 12, 31, 12, 34, 56), '0'))
        self.assertFalse(self.test_data[1] == FileInfo('HOST', 'USER', 0, datetime(2014, 12, 31, 12, 34, 56), '0'))
        self.assertFalse(self.test_data[0] == FileInfo('HOSTx', 'USER', 0, datetime(2014, 12, 31, 12, 34, 56), '0'))
        self.assertFalse(self.test_data[0] == FileInfo('HOST', 'USERx', 0, datetime(2014, 12, 31, 12, 34, 56), '0'))
        self.assertFalse(self.test_data[0] == FileInfo('HOST', 'USER', 1, datetime(2014, 12, 31, 12, 34, 56), '0'))
        self.assertFalse(self.test_data[0] == FileInfo('HOST', 'USER', 0, datetime(2014, 12, 31, 12, 34, 56, 1), '0'))
        self.assertFalse(self.test_data[0] == FileInfo('HOST', 'USER', 0, datetime(2014, 12, 31, 12, 34, 56, 1), '1'))

    def test_ne(self):
        self.assertFalse(self.test_data[0] != FileInfo('HOST', 'USER', 0, datetime(2014, 12, 31, 12, 34, 56), '0'))
        self.assertTrue(self.test_data[1] != FileInfo('HOST', 'USER', 0, datetime(2014, 12, 31, 12, 34, 56), '0'))
        self.assertTrue(self.test_data[0] != FileInfo('HOSTx', 'USER', 0, datetime(2014, 12, 31, 12, 34, 56), '0'))
        self.assertTrue(self.test_data[0] != FileInfo('HOST', 'USERx', 0, datetime(2014, 12, 31, 12, 34, 56), '0'))
        self.assertTrue(self.test_data[0] != FileInfo('HOST', 'USER', 1, datetime(2014, 12, 31, 12, 34, 56), '0'))
        self.assertTrue(self.test_data[0] != FileInfo('HOST', 'USER', 0, datetime(2014, 12, 31, 12, 34, 56, 1), '0'))
        self.assertTrue(self.test_data[0] != FileInfo('HOST', 'USER', 0, datetime(2014, 12, 31, 12, 34, 56, 1), '1'))

    def test_str(self):
        expected = [
            'File Info:\n  User    : USER@HOST\n  Modified: 2014-12-31 12:34:56\n  Size    : 0 (0.0B)\n  MD5     : 0',
            'File Info:\n  User    : USER@HOST\n  Modified: 2014-12-31 12:34:56\n' +
            '  Size    : 10000000000000000000000000000 (8271.8YiB)\n  MD5     : ffff',
        ]
        self.assertEqual(str(self.test_data[0]), expected[0])
        self.assertEqual(str(self.test_data[1]), expected[1])

    def test_repr(self):
        self.assertEqual(repr(self.test_data[0]),
                         "FileInfo(host='HOST', user='USER', size=0, " +
                         "mtime=datetime.datetime(2014, 12, 31, 12, 34, 56), md5='0')")

    def test_from_path(self):
        fi = FileInfo.from_path('tests/resources/test-artifact-1.2.3.dat')
        self.assertEqual((fi.size, fi.md5), (11, '7a38cb250db7127113e00ad5e241d563'))

    def test_dict_conversions(self):
        self.assertEqual(FileInfo.from_dict(self.test_data[0].to_dict()), self.test_data[0])
        self.assertEqual(FileInfo.from_dict(self.test_data[1].to_dict()), self.test_data[1])
