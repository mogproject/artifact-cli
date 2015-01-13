import unittest
from datetime import datetime
from artifactcli.artifact import GitInfo


class TestGitInfo(unittest.TestCase):
    def setUp(self):
        self.test_data = [
            GitInfo('master', [], 'AUTHOR', 'x@example.com', datetime(2014, 12, 31, 12, 34, 56),
                    'COMMIT MSG', 'ffff'),
            GitInfo('master', ['release_YYYYMMDD', 'TAG'], 'AUTHOR', 'y@example.com',
                    datetime(2014, 12, 31, 12, 34, 56), 'COMMIT MSG', '0123'),
        ]

    def test_eq(self):
        self.assertTrue(self.test_data[0] == GitInfo('master', [], 'AUTHOR', 'x@example.com',
                                                     datetime(2014, 12, 31, 12, 34, 56), 'COMMIT MSG', 'ffff'))
        self.assertFalse(self.test_data[1] == GitInfo('master', [], 'AUTHOR', 'x@example.com',
                                                      datetime(2014, 12, 31, 12, 34, 56), 'COMMIT MSG', 'ffff'))
        self.assertFalse(self.test_data[0] == GitInfo('masterX', [], 'AUTHOR', 'x@example.com',
                                                      datetime(2014, 12, 31, 12, 34, 56), 'COMMIT MSG', 'ffff'))
        self.assertFalse(self.test_data[0] == GitInfo('master', [], 'AUTHORX', 'x@example.com',
                                                      datetime(2014, 12, 31, 12, 34, 56), 'COMMIT MSG', 'ffff'))
        self.assertFalse(self.test_data[0] == GitInfo('master', [], 'AUTHOR', 'y@example.com',
                                                      datetime(2014, 12, 31, 12, 34, 56), 'COMMIT MSG', 'ffff'))
        self.assertFalse(self.test_data[0] == GitInfo('master', [], 'AUTHOR', 'x@example.com',
                                                      datetime(2014, 12, 31, 12, 34, 56, 1), 'COMMIT MSG', 'ffff'))
        self.assertFalse(self.test_data[0] == GitInfo('master', [], 'AUTHOR', 'x@example.com',
                                                      datetime(2014, 12, 31, 12, 34, 56), 'COMMIT MSGX', 'ffff'))
        self.assertFalse(self.test_data[0] == GitInfo('master', [], 'AUTHOR', 'x@example.com',
                                                      datetime(2014, 12, 31, 12, 34, 56), 'COMMIT MSG', 'fffe'))

    def test_ne(self):
        self.assertFalse(self.test_data[0] != GitInfo('master', [], 'AUTHOR', 'x@example.com',
                                                      datetime(2014, 12, 31, 12, 34, 56), 'COMMIT MSG', 'ffff'))
        self.assertTrue(self.test_data[1] != GitInfo('master', [], 'AUTHOR', 'x@example.com',
                                                     datetime(2014, 12, 31, 12, 34, 56), 'COMMIT MSG', 'ffff'))
        self.assertTrue(self.test_data[0] != GitInfo('masterX', [], 'AUTHOR', 'x@example.com',
                                                     datetime(2014, 12, 31, 12, 34, 56), 'COMMIT MSG', 'ffff'))
        self.assertTrue(self.test_data[0] != GitInfo('master', [], 'AUTHORX', 'x@example.com',
                                                     datetime(2014, 12, 31, 12, 34, 56), 'COMMIT MSG', 'ffff'))
        self.assertTrue(self.test_data[0] != GitInfo('master', [], 'AUTHOR', 'y@example.com',
                                                     datetime(2014, 12, 31, 12, 34, 56), 'COMMIT MSG', 'ffff'))
        self.assertTrue(self.test_data[0] != GitInfo('master', [], 'AUTHOR', 'x@example.com',
                                                     datetime(2014, 12, 31, 12, 34, 56, 1), 'COMMIT MSG', 'ffff'))
        self.assertTrue(self.test_data[0] != GitInfo('master', [], 'AUTHOR', 'x@example.com',
                                                     datetime(2014, 12, 31, 12, 34, 56), 'COMMIT MSGX', 'ffff'))
        self.assertTrue(self.test_data[0] != GitInfo('master', [], 'AUTHOR', 'x@example.com',
                                                     datetime(2014, 12, 31, 12, 34, 56), 'COMMIT MSG', 'fffe'))

    def test_str_type(self):
        self.assertTrue(all(isinstance(x.__str__(), str) for x in self.test_data))

    def test_repr(self):
        self.assertEqual(repr(self.test_data[0]),
                         "GitInfo(branch='master', tags=[], author_name='AUTHOR', author_email='x@example.com', " +
                         "committed_date=datetime.datetime(2014, 12, 31, 12, 34, 56), summary='COMMIT MSG', " +
                         "sha='ffff')")
        self.assertEqual(repr(self.test_data[1]),
                         "GitInfo(branch='master', tags=['release_YYYYMMDD', 'TAG'], author_name='AUTHOR', " +
                         "author_email='y@example.com', committed_date=datetime.datetime(2014, 12, 31, 12, 34, 56), " +
                         "summary='COMMIT MSG', sha='0123')")

    def test_from_path(self):
        gi = GitInfo.from_path('tests/resources/test-artifact-1.2.3.dat')

    def test_from_path_error(self):
        self.assertEqual(GitInfo.from_path('tests/resources/test001_no_such_path.dat'), None)
        self.assertEqual(GitInfo.from_path('/'), None)

    def test_dict_conversions(self):
        self.assertEqual(GitInfo.from_dict(self.test_data[0].to_dict()), self.test_data[0])
        self.assertEqual(GitInfo.from_dict(self.test_data[1].to_dict()), self.test_data[1])
