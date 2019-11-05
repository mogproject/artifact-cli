# -*- encoding: utf-8 -*-

import unittest
from datetime import datetime
from io import StringIO
import json

from artifactcli.artifact import *
from artifactcli.driver import *
from artifactcli.repository import Repository


class TestRepository(unittest.TestCase):
    def setUp(self):
        self.artifacts_for_test = [
            Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.1', 'jar', 123),
                     FileInfo('host1', 'user1', 4567890, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'first commit',
                             '111122223333444455556666777788889999aaaa')),
            Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.1', 'jar', 124),
                     FileInfo('host1', 'user1', 22222, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'second commit',
                             '111122223333444455556666777788889999aaaa')),
            Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.2', 'jar', 125),
                     FileInfo('host1', 'user1', 4567890, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.2'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'new version',
                             '111122223333444455556666777788889999aaaa')),
            Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.1', 'jar', 126),
                     FileInfo('host1', 'user1', 33333, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'third commit',
                             '111122223333444455556666777788889999aaaa')),
            Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.1', 'jar', 1),
                     FileInfo('host1', 'user1', 4567890, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'first commit',
                             '111122223333444455556666777788889999aaaa')),
            Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.1', 'jar', 2),
                     FileInfo('host1', 'user1', 22222, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'second commit',
                             '111122223333444455556666777788889999aaaa')),
            Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.2', 'jar', 1),
                     FileInfo('host1', 'user1', 4567890, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.2'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'new version',
                             '111122223333444455556666777788889999aaaa')),
            Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.1', 'jar', 3),
                     FileInfo('host1', 'user1', 33333, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'third commit',
                             '111122223333444455556666777788889999aaaa')),
            Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.1', 'jar', 4),
                     FileInfo('host1', 'user1', 44444, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     None),
            Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.1', 'jar', 127),
                     FileInfo('host1', 'user1', 4567890, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.1'], u'あいう', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), u'かきく',
                             '111122223333444455556666777788889999aaaa')),
        ]
        self.maxDiff = None

    def __mock_repo(self):
        return Repository(MockDriver(), 'com.github.mogproject')

    def test_load(self):
        r = self.__mock_repo()
        r.load('art-test')
        self.assertEqual(r.artifacts, {'art-test': []})

    def test_load_all(self):
        r = self.__mock_repo()
        r.load_all()
        self.assertEqual(r.artifacts, {})

    def test_save(self):
        r = self.__mock_repo()
        r.artifacts['art-test'] += self.artifacts_for_test
        r.save('art-test')

        r.artifacts = {}
        r.load_all()
        self.assertEqual(r.artifacts, {'art-test': self.artifacts_for_test})

    #
    # upload
    #
    def test_upload_new_artifact(self):
        expected = [Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.1', 'jar', 1),
                             FileInfo('host1', 'user1', 4567890, datetime(2014, 12, 31, 9, 12, 34),
                                      'ffffeeeeddddccccbbbbaaaa99998888'),
                             GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                                     datetime(2014, 12, 30, 8, 11, 29), 'first commit',
                                     '111122223333444455556666777788889999aaaa'))]
        r = self.__mock_repo()
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[0])

        self.assertEqual(r.artifacts, {'art-test': expected})

    def test_upload_duplicated_artifact(self):
        expected = [Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.1', 'jar', 1),
                             FileInfo('host1', 'user1', 4567890, datetime(2014, 12, 31, 9, 12, 34),
                                      'ffffeeeeddddccccbbbbaaaa99998888'),
                             GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                                     datetime(2014, 12, 30, 8, 11, 29), 'first commit',
                                     '111122223333444455556666777788889999aaaa'))]
        r = self.__mock_repo()
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[0])
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[0])

        self.assertEqual(r.artifacts, {'art-test': expected})

    def test_upload_several_revisions(self):
        r = self.__mock_repo()
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[0])
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[1])
        r.upload('/path/to/art-test-0.0.2.jar', self.artifacts_for_test[2])
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[3])

        self.assertEqual(r.artifacts, {'art-test': [
            Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.1', 'jar', 1),
                     FileInfo('host1', 'user1', 4567890, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'first commit',
                             '111122223333444455556666777788889999aaaa')),
            Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.1', 'jar', 2),
                     FileInfo('host1', 'user1', 22222, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'second commit',
                             '111122223333444455556666777788889999aaaa')),
            Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.2', 'jar', 1),
                     FileInfo('host1', 'user1', 4567890, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.2'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'new version',
                             '111122223333444455556666777788889999aaaa')),
            Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.1', 'jar', 3),
                     FileInfo('host1', 'user1', 33333, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'third commit',
                             '111122223333444455556666777788889999aaaa')),
        ]})

    def test_upload_file_real_file(self):
        r = self.__mock_repo()
        r.upload('tests/resources/test-artifact-1.2.3.dat')

        self.assertEqual(len(r.artifacts['test-artifact']), 1)

        ret = r.artifacts['test-artifact'][0]
        self.assertEqual(ret.basic_info, BasicInfo('com.github.mogproject', 'test-artifact', '1.2.3', 'dat', 1))
        self.assertEqual((ret.file_info.size, ret.file_info.md5), (11, '7a38cb250db7127113e00ad5e241d563'))
        self.assertFalse(ret.scm_info is None)

    def test_upload_file_force(self):
        expected = [Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.1', 'jar', 1),
                             FileInfo('host1', 'user1', 4567890, datetime(2014, 12, 31, 9, 12, 34),
                                      'ffffeeeeddddccccbbbbaaaa99998888'),
                             GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                                     datetime(2014, 12, 30, 8, 11, 29), 'first commit',
                                     '111122223333444455556666777788889999aaaa')),
                    Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.1', 'jar', 2),
                             FileInfo('host1', 'user1', 4567890, datetime(2014, 12, 31, 9, 12, 34),
                                      'ffffeeeeddddccccbbbbaaaa99998888'),
                             GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                                     datetime(2014, 12, 30, 8, 11, 29), 'first commit',
                                     '111122223333444455556666777788889999aaaa'))]
        r = self.__mock_repo()
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[0])
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[0], force=True)

        self.assertEqual(r.artifacts, {'art-test': expected})

    def test_upload_file_print_only(self):
        r = self.__mock_repo()
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[0], print_only=True)

        self.assertEqual(r.artifacts, {})

    def test_upload_file_force_print_only(self):
        expected = [Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.1', 'jar', 1),
                             FileInfo('host1', 'user1', 4567890, datetime(2014, 12, 31, 9, 12, 34),
                                      'ffffeeeeddddccccbbbbaaaa99998888'),
                             GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                                     datetime(2014, 12, 30, 8, 11, 29), 'first commit',
                                     '111122223333444455556666777788889999aaaa'))]
        r = self.__mock_repo()
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[0])
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[0], force=True, print_only=True)

        self.assertEqual(r.artifacts, {'art-test': expected})

    #
    # download
    #
    def test_download_specified_revision(self):
        r = self.__mock_repo()
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[0])
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[1])
        r.upload('/path/to/art-test-0.0.2.jar', self.artifacts_for_test[2])
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[3])

        r.download('/tmp/art-test-0.0.1.jar', 2)
        self.assertEqual(r.driver.downloaded_data, {
            '/tmp/art-test-0.0.1.jar': ('com.github.mogproject/art-test/0.0.1/2/art-test-0.0.1.jar',
                                        'ffffeeeeddddccccbbbbaaaa99998888')})

    def test_download_latest_revision(self):
        r = self.__mock_repo()
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[0])
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[1])
        r.upload('/path/to/art-test-0.0.2.jar', self.artifacts_for_test[2])
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[3])

        r.download('/tmp/art-test-0.0.1.jar', None)
        self.assertEqual(r.driver.downloaded_data, {
            '/tmp/art-test-0.0.1.jar': ('com.github.mogproject/art-test/0.0.1/3/art-test-0.0.1.jar',
                                        'ffffeeeeddddccccbbbbaaaa99998888')})

    def test_download_print_only(self):
        r = self.__mock_repo()
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[0])
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[1])
        r.upload('/path/to/art-test-0.0.2.jar', self.artifacts_for_test[2])
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[3])

        r.download('/tmp/art-test-0.0.1.jar', 2, print_only=True)
        r.download('/tmp/art-test-0.0.1.jar', None, print_only=True)
        self.assertEqual(r.driver.downloaded_data, {})

    def test_download_no_such_revision(self):
        r = self.__mock_repo()
        self.assertRaises(ValueError, r.download, '/tmp/art-test-0.0.1.jar', None)
        self.assertRaises(ValueError, r.download, '/tmp/art-test-0.0.1.jar', 123)

    def test_download_broken_index_error(self):
        r = self.__mock_repo()
        r.artifacts = {'art-test': [
            Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.1', 'jar', 123),
                     FileInfo('host1', 'user1', 4567890, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'first commit',
                             '111122223333444455556666777788889999aaaa')),
            Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.1', 'jar', 123),
                     FileInfo('host1', 'user1', 4567890, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'first commit',
                             '111122223333444455556666777788889999aaaa')),
        ]}
        self.assertRaises(ValueError, r.download, '/tmp/art-test-0.0.1.jar', 123)

    #
    # delete
    #
    def test_delete_specified_revision(self):
        r = self.__mock_repo()
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[0])
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[1])
        r.upload('/path/to/art-test-0.0.2.jar', self.artifacts_for_test[2])
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[3])

        r.delete('art-test-0.0.1.jar', 2)
        self.assertEqual(r.driver.uploaded_data, {
            'com.github.mogproject/art-test/0.0.1/1/art-test-0.0.1.jar': (
                '/path/to/art-test-0.0.1.jar', 'ffffeeeeddddccccbbbbaaaa99998888'),
            'com.github.mogproject/art-test/0.0.1/3/art-test-0.0.1.jar': (
                '/path/to/art-test-0.0.1.jar', 'ffffeeeeddddccccbbbbaaaa99998888'),
            'com.github.mogproject/art-test/0.0.2/1/art-test-0.0.2.jar': (
                '/path/to/art-test-0.0.2.jar', 'ffffeeeeddddccccbbbbaaaa99998888')
        })

        expected = [
            Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.1', 'jar', 1),
                     FileInfo('host1', 'user1', 4567890, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'first commit',
                             '111122223333444455556666777788889999aaaa')),
            Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.2', 'jar', 1),
                     FileInfo('host1', 'user1', 4567890, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.2'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'new version',
                             '111122223333444455556666777788889999aaaa')),
            Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.1', 'jar', 3),
                     FileInfo('host1', 'user1', 33333, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'third commit',
                             '111122223333444455556666777788889999aaaa')),
        ]
        self.assertEqual(r.artifacts, {'art-test': expected})

    def test_delete_revision_can_be_reused(self):
        r = self.__mock_repo()

        # [] -> [1] -> []
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[0])
        r.delete('art-test-0.0.1.jar', 1)
        self.assertEqual(r.artifacts, {'art-test': []})

        # [] -> [1]
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[0])
        self.assertEqual(r.artifacts, {'art-test': [
            Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.1', 'jar', 1),
                     FileInfo('host1', 'user1', 4567890, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'first commit',
                             '111122223333444455556666777788889999aaaa')),
        ]})

        # [1] -> [1, 2] -> [2]
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[1])
        r.delete('art-test-0.0.1.jar', 1)
        self.assertEqual(r.artifacts, {'art-test': [
            Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.1', 'jar', 2),
                     FileInfo('host1', 'user1', 22222, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'second commit',
                             '111122223333444455556666777788889999aaaa')),
        ]})

        # [2] -> [2, 3]
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[3])
        self.assertEqual(r.artifacts, {'art-test': [
            Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.1', 'jar', 2),
                     FileInfo('host1', 'user1', 22222, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'second commit',
                             '111122223333444455556666777788889999aaaa')),

            Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.1', 'jar', 3),
                     FileInfo('host1', 'user1', 33333, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'third commit',
                             '111122223333444455556666777788889999aaaa')),
        ]})

        # [2, 3] -> [2] -> [2, 3]
        r.delete('art-test-0.0.1.jar', 3)
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[3])
        self.assertEqual(r.artifacts, {'art-test': [
            Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.1', 'jar', 2),
                     FileInfo('host1', 'user1', 22222, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'second commit',
                             '111122223333444455556666777788889999aaaa')),

            Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.1', 'jar', 3),
                     FileInfo('host1', 'user1', 33333, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'third commit',
                             '111122223333444455556666777788889999aaaa')),
        ]})

    def test_delete_revision_not_specified(self):
        r = self.__mock_repo()
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[0])
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[1])
        r.upload('/path/to/art-test-0.0.2.jar', self.artifacts_for_test[2])
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[3])

        self.assertRaises(ValueError, r.delete, 'art-test-0.0.1.jar', None)

        self.assertEqual(r.driver.uploaded_data, {
            'com.github.mogproject/art-test/0.0.1/1/art-test-0.0.1.jar': (
                '/path/to/art-test-0.0.1.jar', 'ffffeeeeddddccccbbbbaaaa99998888'),
            'com.github.mogproject/art-test/0.0.1/2/art-test-0.0.1.jar': (
                '/path/to/art-test-0.0.1.jar', 'ffffeeeeddddccccbbbbaaaa99998888'),
            'com.github.mogproject/art-test/0.0.1/3/art-test-0.0.1.jar': (
                '/path/to/art-test-0.0.1.jar', 'ffffeeeeddddccccbbbbaaaa99998888'),
            'com.github.mogproject/art-test/0.0.2/1/art-test-0.0.2.jar': (
                '/path/to/art-test-0.0.2.jar', 'ffffeeeeddddccccbbbbaaaa99998888')
        })

        expected = [
            Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.1', 'jar', 1),
                     FileInfo('host1', 'user1', 4567890, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'first commit',
                             '111122223333444455556666777788889999aaaa')),
            Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.1', 'jar', 2),
                     FileInfo('host1', 'user1', 22222, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'second commit',
                             '111122223333444455556666777788889999aaaa')),
            Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.2', 'jar', 1),
                     FileInfo('host1', 'user1', 4567890, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.2'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'new version',
                             '111122223333444455556666777788889999aaaa')),
            Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.1', 'jar', 3),
                     FileInfo('host1', 'user1', 33333, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'third commit',
                             '111122223333444455556666777788889999aaaa')),
        ]
        self.assertEqual(r.artifacts, {'art-test': expected})

    def test_delete_print_only(self):
        r = self.__mock_repo()
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[0])
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[1])
        r.upload('/path/to/art-test-0.0.2.jar', self.artifacts_for_test[2])
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[3])

        r.delete('art-test-0.0.1.jar', 2, print_only=True)
        self.assertEqual(r.driver.uploaded_data, {
            'com.github.mogproject/art-test/0.0.1/1/art-test-0.0.1.jar': (
                '/path/to/art-test-0.0.1.jar', 'ffffeeeeddddccccbbbbaaaa99998888'),
            'com.github.mogproject/art-test/0.0.1/2/art-test-0.0.1.jar': (
                '/path/to/art-test-0.0.1.jar', 'ffffeeeeddddccccbbbbaaaa99998888'),
            'com.github.mogproject/art-test/0.0.1/3/art-test-0.0.1.jar': (
                '/path/to/art-test-0.0.1.jar', 'ffffeeeeddddccccbbbbaaaa99998888'),
            'com.github.mogproject/art-test/0.0.2/1/art-test-0.0.2.jar': (
                '/path/to/art-test-0.0.2.jar', 'ffffeeeeddddccccbbbbaaaa99998888')
        })

        expected = [
            Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.1', 'jar', 1),
                     FileInfo('host1', 'user1', 4567890, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'first commit',
                             '111122223333444455556666777788889999aaaa')),
            Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.1', 'jar', 2),
                     FileInfo('host1', 'user1', 22222, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'second commit',
                             '111122223333444455556666777788889999aaaa')),
            Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.2', 'jar', 1),
                     FileInfo('host1', 'user1', 4567890, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.2'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'new version',
                             '111122223333444455556666777788889999aaaa')),
            Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.1', 'jar', 3),
                     FileInfo('host1', 'user1', 33333, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'third commit',
                             '111122223333444455556666777788889999aaaa')),
        ]
        self.assertEqual(r.artifacts, {'art-test': expected})

    def test_delete_no_such_revision(self):
        r = self.__mock_repo()
        self.assertRaises(ValueError, r.delete, 'art-test-0.0.1.jar', 123)

    def test_delete_broken_index_error(self):
        r = self.__mock_repo()
        r.artifacts = {'art-test': [
            Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.1', 'jar', 123),
                     FileInfo('host1', 'user1', 4567890, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'first commit',
                             '111122223333444455556666777788889999aaaa')),
            Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.1', 'jar', 123),
                     FileInfo('host1', 'user1', 4567890, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'first commit',
                             '111122223333444455556666777788889999aaaa')),
        ]}
        self.assertRaises(ValueError, r.delete, 'art-test-0.0.1.jar', 123)

    #
    # print_list
    #
    def test_print_list_empty(self):
        r = self.__mock_repo()
        r.print_list()

    def test_print_list_output_text(self):
        r = self.__mock_repo()
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[0])
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[1])
        r.upload('/path/to/art-test-0.0.2.jar', self.artifacts_for_test[2])
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[3])
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[8])
        fp = StringIO()
        r.print_list(fp=fp)
        self.assertEqual(fp.getvalue(), '\n'.join([
            'FILE                   #    SIZE      BUILD                 TAGS            SUMMARY        ',
            '-------------------------------------------------------------------------------------------',
            'art-test-0.0.1.jar      1   4.4MiB    2014-12-31 09:12:34   release 0.0.1   first commit   ',
            'art-test-0.0.1.jar      2   21.7KiB   2014-12-31 09:12:34   release 0.0.1   second commit  ',
            'art-test-0.0.1.jar      3   32.6KiB   2014-12-31 09:12:34   release 0.0.1   third commit   ',
            'art-test-0.0.1.jar      4   43.4KiB   2014-12-31 09:12:34                                  ',
            'art-test-0.0.2.jar      1   4.4MiB    2014-12-31 09:12:34   release 0.0.2   new version    ',
        ]) + '\n')
        fp.close()

    def test_print_list_output_text_long(self):
        r = self.__mock_repo()
        for i in range(15):
            r.upload('/path/to/art-test-0.0.2.jar', self.artifacts_for_test[2], True)
            r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[0], True)
        fp = StringIO()
        r.print_list(fp=fp)
        self.assertEqual(fp.getvalue(), '\n'.join([
            'FILE                   #    SIZE     BUILD                 TAGS            SUMMARY       ',
            '-----------------------------------------------------------------------------------------',
            'art-test-0.0.1.jar      1   4.4MiB   2014-12-31 09:12:34   release 0.0.1   first commit  ',
            'art-test-0.0.1.jar      2   4.4MiB   2014-12-31 09:12:34   release 0.0.1   first commit  ',
            'art-test-0.0.1.jar      3   4.4MiB   2014-12-31 09:12:34   release 0.0.1   first commit  ',
            'art-test-0.0.1.jar      4   4.4MiB   2014-12-31 09:12:34   release 0.0.1   first commit  ',
            'art-test-0.0.1.jar      5   4.4MiB   2014-12-31 09:12:34   release 0.0.1   first commit  ',
            'art-test-0.0.1.jar      6   4.4MiB   2014-12-31 09:12:34   release 0.0.1   first commit  ',
            'art-test-0.0.1.jar      7   4.4MiB   2014-12-31 09:12:34   release 0.0.1   first commit  ',
            'art-test-0.0.1.jar      8   4.4MiB   2014-12-31 09:12:34   release 0.0.1   first commit  ',
            'art-test-0.0.1.jar      9   4.4MiB   2014-12-31 09:12:34   release 0.0.1   first commit  ',
            'art-test-0.0.1.jar     10   4.4MiB   2014-12-31 09:12:34   release 0.0.1   first commit  ',
            'art-test-0.0.1.jar     11   4.4MiB   2014-12-31 09:12:34   release 0.0.1   first commit  ',
            'art-test-0.0.1.jar     12   4.4MiB   2014-12-31 09:12:34   release 0.0.1   first commit  ',
            'art-test-0.0.1.jar     13   4.4MiB   2014-12-31 09:12:34   release 0.0.1   first commit  ',
            'art-test-0.0.1.jar     14   4.4MiB   2014-12-31 09:12:34   release 0.0.1   first commit  ',
            'art-test-0.0.1.jar     15   4.4MiB   2014-12-31 09:12:34   release 0.0.1   first commit  ',
            'art-test-0.0.2.jar      1   4.4MiB   2014-12-31 09:12:34   release 0.0.2   new version   ',
            'art-test-0.0.2.jar      2   4.4MiB   2014-12-31 09:12:34   release 0.0.2   new version   ',
            'art-test-0.0.2.jar      3   4.4MiB   2014-12-31 09:12:34   release 0.0.2   new version   ',
            'art-test-0.0.2.jar      4   4.4MiB   2014-12-31 09:12:34   release 0.0.2   new version   ',
            'art-test-0.0.2.jar      5   4.4MiB   2014-12-31 09:12:34   release 0.0.2   new version   ',
            'art-test-0.0.2.jar      6   4.4MiB   2014-12-31 09:12:34   release 0.0.2   new version   ',
            'art-test-0.0.2.jar      7   4.4MiB   2014-12-31 09:12:34   release 0.0.2   new version   ',
            'art-test-0.0.2.jar      8   4.4MiB   2014-12-31 09:12:34   release 0.0.2   new version   ',
            'art-test-0.0.2.jar      9   4.4MiB   2014-12-31 09:12:34   release 0.0.2   new version   ',
            'art-test-0.0.2.jar     10   4.4MiB   2014-12-31 09:12:34   release 0.0.2   new version   ',
            'art-test-0.0.2.jar     11   4.4MiB   2014-12-31 09:12:34   release 0.0.2   new version   ',
            'art-test-0.0.2.jar     12   4.4MiB   2014-12-31 09:12:34   release 0.0.2   new version   ',
            'art-test-0.0.2.jar     13   4.4MiB   2014-12-31 09:12:34   release 0.0.2   new version   ',
            'art-test-0.0.2.jar     14   4.4MiB   2014-12-31 09:12:34   release 0.0.2   new version   ',
            'art-test-0.0.2.jar     15   4.4MiB   2014-12-31 09:12:34   release 0.0.2   new version   ',
        ]) + '\n')
        fp.close()

    def test_print_list_output_json(self):
        r = self.__mock_repo()
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[0])
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[1])
        r.upload('/path/to/art-test-0.0.2.jar', self.artifacts_for_test[2])
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[3])
        fp = StringIO()
        r.print_list(output='json', fp=fp)
        arts = [Artifact.from_dict(d) for d in json.loads(fp.getvalue())]
        self.assertEqual(arts, [
            Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.1', 'jar', 1),
                     FileInfo('host1', 'user1', 4567890, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'first commit',
                             '111122223333444455556666777788889999aaaa')),
            Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.1', 'jar', 2),
                     FileInfo('host1', 'user1', 22222, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'second commit',
                             '111122223333444455556666777788889999aaaa')),
            Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.1', 'jar', 3),
                     FileInfo('host1', 'user1', 33333, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'third commit',
                             '111122223333444455556666777788889999aaaa')),
            Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.2', 'jar', 1),
                     FileInfo('host1', 'user1', 4567890, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.2'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'new version',
                             '111122223333444455556666777788889999aaaa')),
        ])
        fp.close()

    def test_print_list_output_json_long(self):
        r = self.__mock_repo()
        for i in range(15):
            r.upload('/path/to/art-test-0.0.2.jar', self.artifacts_for_test[2], True)
            r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[0], True)
        fp = StringIO()
        r.print_list(output='json', fp=fp)
        arts = [Artifact.from_dict(d) for d in json.loads(fp.getvalue())]
        a = [
            Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.1', 'jar', i),
                     FileInfo('host1', 'user1', 4567890, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.1'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'first commit',
                             '111122223333444455556666777788889999aaaa'))
            for i in range(1, 16)
        ]
        b = [
            Artifact(BasicInfo('com.github.mogproject', 'art-test', '0.0.2', 'jar', i),
                     FileInfo('host1', 'user1', 4567890, datetime(2014, 12, 31, 9, 12, 34),
                              'ffffeeeeddddccccbbbbaaaa99998888'),
                     GitInfo('master', ['release 0.0.2'], 'mogproject', 'x@example.com',
                             datetime(2014, 12, 30, 8, 11, 29), 'new version',
                             '111122223333444455556666777788889999aaaa'))
            for i in range(1, 16)
        ]
        self.assertEqual(arts, a + b)
        fp.close()

    def test_print_list_output_error(self):
        r = self.__mock_repo()
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[0])
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[1])
        r.upload('/path/to/art-test-0.0.2.jar', self.artifacts_for_test[2])
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[3])
        r.save('art-test')

        self.assertRaises(ValueError, r.print_list, 'xxxx')

    #
    # print_info
    #
    def test_print_info_output_text(self):
        r = self.__mock_repo()
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[4])
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[5])
        r.upload('/path/to/art-test-0.0.2.jar', self.artifacts_for_test[6])
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[7])
        r.save('art-test')

        def f(file_name, revision):
            fp = StringIO()
            r.print_info(file_name, revision, fp=fp)
            ret = fp.getvalue()
            fp.close()
            return ret

        self.assertEqual(f('art-test-0.0.1.jar', 1), str(self.artifacts_for_test[4]) + '\n')
        self.assertEqual(f('art-test-0.0.1.jar', 2), str(self.artifacts_for_test[5]) + '\n')
        self.assertEqual(f('art-test-0.0.2.jar', 1), str(self.artifacts_for_test[6]) + '\n')
        self.assertEqual(f('art-test-0.0.1.jar', 3), str(self.artifacts_for_test[7]) + '\n')
        self.assertEqual(f('art-test-0.0.1.jar', None), str(self.artifacts_for_test[7]) + '\n')
        self.assertEqual(f('art-test-0.0.2.jar', None), str(self.artifacts_for_test[6]) + '\n')

    def test_print_info_output_json(self):
        r = self.__mock_repo()
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[4])
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[5])
        r.upload('/path/to/art-test-0.0.2.jar', self.artifacts_for_test[6])
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[7])
        r.save('art-test')

        def f(file_name, revision):
            fp = StringIO()
            r.print_info(file_name, revision, output='json', fp=fp)
            ret = Artifact.from_dict(json.loads(fp.getvalue()))
            fp.close()
            return ret

        self.assertEqual(f('art-test-0.0.1.jar', 1), self.artifacts_for_test[4])
        self.assertEqual(f('art-test-0.0.1.jar', 2), self.artifacts_for_test[5])
        self.assertEqual(f('art-test-0.0.2.jar', 1), self.artifacts_for_test[6])
        self.assertEqual(f('art-test-0.0.1.jar', 3), self.artifacts_for_test[7])
        self.assertEqual(f('art-test-0.0.1.jar', None), self.artifacts_for_test[7])
        self.assertEqual(f('art-test-0.0.2.jar', None), self.artifacts_for_test[6])

    def test_print_info_output_error(self):
        r = self.__mock_repo()
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[0])
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[1])
        r.upload('/path/to/art-test-0.0.2.jar', self.artifacts_for_test[2])
        r.upload('/path/to/art-test-0.0.1.jar', self.artifacts_for_test[3])
        r.save('art-test')

        self.assertRaises(ValueError, r.print_info, 'art-test-0.0.1.jar', None, 'xxxx')
