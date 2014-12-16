import unittest
from datetime import datetime
from artifactcli import *


class TestListOperation(unittest.TestCase):
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
        r = Repository(MockDriver())
        r.upload('com.github.mogproject', '/path/to/art-test-0.0.1.jar', arts[0])
        r.upload('com.github.mogproject', '/path/to/art-test-0.0.1.jar', arts[1])

        r.artifacts = []

        rc = ListOperation('com.github.mogproject', []).run(r)
        self.assertEqual(rc, 0)
