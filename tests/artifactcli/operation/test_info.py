import unittest
from datetime import datetime
from artifactcli import *


class TestInfoOperation(unittest.TestCase):
    def test_init_error(self):
        self.assertRaises(AssertionError, InfoOperation, 'com.github.mogproject',
                          ['art-test-0.0.1.jar', 'Latest'], False)
        self.assertRaises(AssertionError, InfoOperation, 'com.github.mogproject',
                          ['art-test-0.0.1.jar', '1a'], False)

    def test_run(self):
        arts = [
            Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.1', 'jar', 1),
                     FileInfo('host1', 'user1', 4567890, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'first commit',
                             '111122223333444455556666777788889999aaaa')),
            Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.1', 'jar', 2),
                     FileInfo('host1', 'user1', 4567891, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998887'),
                     GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'first commit',
                             '111122223333444455556666777788889999aaaa')),
        ]
        r = Repository(MockDriver(), 'com.github.mogproject')
        r.upload('/path/to/art-test-0.0.1.jar', arts[0])
        r.upload('/path/to/art-test-0.0.1.jar', arts[1])
        r.save('art-test')

        r.artifacts = {}

        rc = InfoOperation('com.github.mogproject', ['art-test-0.0.1.jar', '1']).run(r)
        self.assertEqual(rc, 0)

        rc = InfoOperation('com.github.mogproject', ['art-test-0.0.1.jar', '2']).run(r)
        self.assertEqual(rc, 0)

        rc = InfoOperation('com.github.mogproject', ['art-test-0.0.1.jar', 'latest']).run(r)
        self.assertEqual(rc, 0)

    def test_run_error(self):
        r = Repository(MockDriver(), 'com.github.mogproject')
        rc = InfoOperation('com.github.mogproject', ['art-test-0.0.1.jar', '1']).run(r)
        self.assertEqual(rc, 2)
