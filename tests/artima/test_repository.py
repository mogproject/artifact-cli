import unittest
from datetime import datetime
import copy
from src.artima import *
from driver.mockdriver import MockDriver


class TestRepository(unittest.TestCase):
    def setUp(self):
        self.artifacts_for_test = [
            Artifact(BasicInfo('com.github.mogproject', 'artima-test', '0.0.1', 'jar', 123),
                     FileInfo('host1', 'user1', 4567890, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'first commit',
                             '111122223333444455556666777788889999aaaa')),
            Artifact(BasicInfo('com.github.mogproject', 'artima-test', '0.0.1', 'jar', 124),
                     FileInfo('host1', 'user1', 22222, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'first commit',
                             '111122223333444455556666777788889999aaaa')),
            Artifact(BasicInfo('com.github.mogproject', 'artima-test', '0.0.2', 'jar', 125),
                     FileInfo('host1', 'user1', 4567890, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'first commit',
                             '111122223333444455556666777788889999aaaa')),
            Artifact(BasicInfo('com.github.mogproject', 'artima-test', '0.0.1', 'jar', 126),
                     FileInfo('host1', 'user1', 33333, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'first commit',
                             '111122223333444455556666777788889999aaaa')),
        ]
        self.maxDiff = None

    def test_load(self):
        r = Repository(MockDriver())
        r.load()
        self.assertEqual(r.artifacts, [])

    def test_save(self):
        r = Repository(MockDriver())
        r.artifacts += self.artifacts_for_test
        r.save()

        r.artifacts = []
        r.load()
        self.assertEqual(r.artifacts, self.artifacts_for_test)

    def test_upload_new_artifact(self):
        expected = Artifact(BasicInfo('com.github.mogproject', 'artima-test', '0.0.1', 'jar', 1),
                            FileInfo('host1', 'user1', 4567890, datetime(2014, 12, 31, 9, 12, 34),
                                     'ffffeeeeddddccccbbbbaaaa99998888'),
                            GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                                    datetime(2014, 12, 30, 8, 11, 29), 'first commit',
                                    '111122223333444455556666777788889999aaaa'))
        r = Repository(MockDriver())
        r.upload('com.github.mogproject', '/path/to/artima-test-0.0.1.jar', self.artifacts_for_test[0])

        self.assertEqual(r.artifacts, [expected])

        # assume artifact is automatically saved
        r.artifacts = []
        r.load()
        self.assertEqual(r.artifacts, [expected])

    def test_upload_duplicated_artifact(self):
        r = Repository(MockDriver())
        r.upload('com.github.mogproject', '/path/to/artima-test-0.0.1.jar', self.artifacts_for_test[0])
        self.assertRaises(
            ValueError, r.upload, 'com.github.mogproject', '/path/to/artima-test-0.0.1.jar', self.artifacts_for_test[0])

    def test_upload_several_revisions(self):
        r = Repository(MockDriver())
        r.upload('com.github.mogproject', '/path/to/artima-test-0.0.1.jar', self.artifacts_for_test[0])
        r.upload('com.github.mogproject', '/path/to/artima-test-0.0.1.jar', self.artifacts_for_test[1])
        r.upload('com.github.mogproject', '/path/to/artima-test-0.0.2.jar', self.artifacts_for_test[2])
        r.upload('com.github.mogproject', '/path/to/artima-test-0.0.1.jar', self.artifacts_for_test[3])

        self.assertEqual(r.artifacts, [
            Artifact(BasicInfo('com.github.mogproject', 'artima-test', '0.0.1', 'jar', 1),
                     FileInfo('host1', 'user1', 4567890, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'first commit',
                             '111122223333444455556666777788889999aaaa')),
            Artifact(BasicInfo('com.github.mogproject', 'artima-test', '0.0.1', 'jar', 2),
                     FileInfo('host1', 'user1', 22222, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'first commit',
                             '111122223333444455556666777788889999aaaa')),
            Artifact(BasicInfo('com.github.mogproject', 'artima-test', '0.0.2', 'jar', 1),
                     FileInfo('host1', 'user1', 4567890, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'first commit',
                             '111122223333444455556666777788889999aaaa')),
            Artifact(BasicInfo('com.github.mogproject', 'artima-test', '0.0.1', 'jar', 3),
                     FileInfo('host1', 'user1', 33333, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'first commit',
                             '111122223333444455556666777788889999aaaa')),
        ])


