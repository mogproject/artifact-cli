import unittest
from datetime import datetime
from artifactcli import *


class TestUploadOperation(unittest.TestCase):
    def test_run(self):
        art = Artifact(BasicInfo('com.github.mogproject', 'test-artifact', '1.2.3', 'dat', 1),
                       FileInfo('host1', 'user1', 4567890, datetime(2014, 12, 31, 9, 12, 34),
                                'ffffeeeeddddccccbbbbaaaa99998888'),
                       GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                               datetime(2014, 12, 30, 8, 11, 29), 'first commit',
                               '111122223333444455556666777788889999aaaa'))
        r = Repository(MockDriver())
        r.artifacts = [art]
        r.save()
        r.artifacts = []

        rc = UploadOperation('com.github.mogproject', ['tests/resources/test-artifact-1.2.3.dat'], False, False).run(r)
        self.assertEqual(rc, 0)

        self.assertEqual(len(r.artifacts), 2)
        self.assertEqual(r.artifacts[0], art)

        ret = r.artifacts[1]
        self.assertEqual(ret.basic_info, BasicInfo('com.github.mogproject', 'test-artifact', '1.2.3', 'dat', 2))
        self.assertEqual((ret.file_info.size, ret.file_info.md5), (11, '7a38cb250db7127113e00ad5e241d563'))
        self.assertFalse(ret.scm_info is None)
