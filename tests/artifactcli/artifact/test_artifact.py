import unittest
from datetime import datetime
from artifactcli.artifact import Artifact, BasicInfo, FileInfo, GitInfo


class TestArtifactInfo(unittest.TestCase):
    def setUp(self):
        self.test_bi = [
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', None),
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1.2', 'zip', 345),
        ]
        self.test_fi = [
            FileInfo('HOST', 'USER', 0, datetime(2014, 12, 31, 12, 34, 56), '0'),
            FileInfo('HOST', 'USER', 10000000000000000000000000000, datetime(2014, 12, 31, 12, 34, 56), 'ffff'),
        ]
        self.test_si = [
            GitInfo('master', [], 'AUTHOR', 'x@example.com', datetime(2014, 12, 31, 12, 34, 56),
                    'COMMIT MSG', 'ffff'),
            GitInfo('master', ['release_YYYYMMDD', 'TAG'], 'AUTHOR', 'y@example.com',
                    datetime(2014, 12, 31, 12, 34, 56), 'COMMIT MSG', '0123'),
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
