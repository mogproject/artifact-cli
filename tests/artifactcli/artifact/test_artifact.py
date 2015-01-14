# -*- encoding: utf-8 -*-

import unittest
from datetime import datetime
from artifactcli.artifact import Artifact, BasicInfo, FileInfo, GitInfo


class TestArtifactInfo(unittest.TestCase):
    def setUp(self):
        self.test_bi = [
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', None),
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', u'0.1.2あ', 'zip', 345),
        ]
        self.test_fi = [
            FileInfo('HOST', 'USER', 0, datetime(2014, 12, 31, 12, 34, 56), '0'),
            FileInfo('HOST', u'USERあ', 10000000000000000000000000000, datetime(2014, 12, 31, 12, 34, 56), 'ffff'),
        ]
        self.test_si = [
            GitInfo('master', [], 'AUTHOR', 'x@example.com', datetime(2014, 12, 31, 12, 34, 56),
                    'COMMIT MSG', 'ffff'),
            GitInfo('master', ['release_YYYYMMDD', 'TAG'], u'AUTHORあいう', 'y@example.com',
                    datetime(2014, 12, 31, 12, 34, 56), u'COMMIT MSGかきく', '0123'),
        ]
        self.test_data = [
            Artifact(self.test_bi[0], self.test_fi[0], self.test_si[0]),
            Artifact(self.test_bi[1], self.test_fi[1], self.test_si[1]),
            Artifact(self.test_bi[0], self.test_fi[0], None),
        ]

    def test_eq(self):
        self.assertTrue(
            Artifact(self.test_bi[0], self.test_fi[0], None) == Artifact(self.test_bi[0], self.test_fi[0], None))
        self.assertTrue(
            Artifact(self.test_bi[0], self.test_fi[0], self.test_si[0]) ==
            Artifact(self.test_bi[0], self.test_fi[0], self.test_si[0]))
        self.assertTrue(
            Artifact(self.test_bi[1], self.test_fi[1], self.test_si[1]) ==
            Artifact(self.test_bi[1], self.test_fi[1], self.test_si[1]))
        self.assertFalse(
            Artifact(self.test_bi[0], self.test_fi[0], self.test_si[0]) ==
            Artifact(self.test_bi[1], self.test_fi[1], self.test_si[1]))
        self.assertFalse(
            Artifact(self.test_bi[0], self.test_fi[0], self.test_si[0]) ==
            Artifact(self.test_bi[0], self.test_fi[1], self.test_si[0]))
        self.assertFalse(
            Artifact(self.test_bi[0], self.test_fi[0], self.test_si[0]) ==
            Artifact(self.test_bi[0], self.test_fi[0], self.test_si[1]))

    def test_ne(self):
        self.assertFalse(
            Artifact(self.test_bi[0], self.test_fi[0], None) != Artifact(self.test_bi[0], self.test_fi[0], None))
        self.assertFalse(
            Artifact(self.test_bi[0], self.test_fi[0], self.test_si[0]) !=
            Artifact(self.test_bi[0], self.test_fi[0], self.test_si[0]))
        self.assertFalse(
            Artifact(self.test_bi[1], self.test_fi[1], self.test_si[1]) !=
            Artifact(self.test_bi[1], self.test_fi[1], self.test_si[1]))
        self.assertTrue(
            Artifact(self.test_bi[0], self.test_fi[0], self.test_si[0]) !=
            Artifact(self.test_bi[1], self.test_fi[1], self.test_si[1]))
        self.assertTrue(
            Artifact(self.test_bi[0], self.test_fi[0], self.test_si[0]) !=
            Artifact(self.test_bi[0], self.test_fi[1], self.test_si[0]))
        self.assertTrue(
            Artifact(self.test_bi[0], self.test_fi[0], self.test_si[0]) !=
            Artifact(self.test_bi[0], self.test_fi[0], self.test_si[1]))

    def test_str_type(self):
        self.assertTrue(all(isinstance(x.__str__(), str) for x in self.test_data))

    def test_str(self):
        expected = '\n'.join([
            'Basic Info:',
            '  Group ID   : com.github.mogproject',
            '  Artifact ID: xxx-yyy-assembly',
            u'  Version    : 0.1.2あ',
            '  Packaging  : zip',
            '  Revision   : 345',
            'File Info:',
            u'  User    : USERあ@HOST',
            '  Modified: 2014-12-31 12:34:56',
            '  Size    : 10000000000000000000000000000 (8271.8YiB)',
            '  MD5     : ffff',
            'Git Info:',
            '  Branch             : master',
            '  Tags               : release_YYYYMMDD, TAG',
            u'  Last Commit Author : AUTHORあいう <y@example.com>',
            '  Last Commit Date   : 2014-12-31 12:34:56',
            u'  Last Commit Summary: COMMIT MSGかきく',
            '  Last Commit SHA    : 0123',
        ])
        self.assertEqual(str(self.test_data[1]), expected.encode('utf-8'))

    def test_str_no_scm_info(self):
        expected = '\n'.join([
            'Basic Info:',
            '  Group ID   : com.github.mogproject',
            '  Artifact ID: xxx-yyy-assembly',
            '  Version    : 0.1-SNAPSHOT',
            '  Packaging  : jar',
            '  Revision   : None',
            'File Info:',
            '  User    : USER@HOST',
            '  Modified: 2014-12-31 12:34:56',
            '  Size    : 0 (0.0B)',
            '  MD5     : 0',
        ])
        self.assertEqual(str(self.test_data[2]), expected.encode('utf-8'))

    def test_repr(self):
        self.assertEqual(
            repr(self.test_data[0]),
            'Artifact(basic_info=%r, file_info=%r, scm_info=%r)' % (self.test_bi[0], self.test_fi[0], self.test_si[0]))
        self.assertEqual(
            repr(self.test_data[1]),
            'Artifact(basic_info=%r, file_info=%r, scm_info=%r)' % (self.test_bi[1], self.test_fi[1], self.test_si[1]))

    def test_from_path(self):
        ret = Artifact.from_path('GROUP_ID', 'tests/resources/test-artifact-1.2.3.dat')
        self.assertEqual(ret.basic_info, BasicInfo('GROUP_ID', 'test-artifact', '1.2.3', 'dat', None))
        self.assertEqual((ret.file_info.size, ret.file_info.md5), (11, '7a38cb250db7127113e00ad5e241d563'))
        self.assertFalse(ret.scm_info is None)

    def test_dict_conversions(self):
        self.assertEqual(Artifact.from_dict(self.test_data[0].to_dict()), self.test_data[0])
        self.assertEqual(Artifact.from_dict(self.test_data[1].to_dict()), self.test_data[1])
        self.assertEqual(Artifact.from_dict(self.test_data[2].to_dict()), self.test_data[2])
