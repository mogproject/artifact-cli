# -*- encoding: utf-8 -*-

import unittest
import os
import boto3
from moto import mock_s3
from artifactcli.driver import S3Driver


class TestS3Driver(unittest.TestCase):
    def setUp(self):
        self.tmp_path = 'tests/resources/test-artifact-1.2.3.dat.tmp'

    def _get_driver(self):
        session = boto3.session.Session(aws_access_key_id='XXX', aws_secret_access_key='YYY')
        session.resource('s3').Bucket('bucket4art').create()
        return S3Driver('XXX', 'YYY', 'bucket4art', 'gid', session=session)

    @mock_s3
    def test_get_artifact_ids_empty(self):
        self.assertEqual(self._get_driver().artifact_ids(), [])

    @mock_s3
    def test_get_artifact_ids(self):
        d = self._get_driver()
        d.write_index('test-artifact', '')
        d.write_index('test-artifact123', '')
        d.write_index('test-artifact10', '')
        d.write_index('test-artifact11', '')

        self.assertEqual(d.artifact_ids(), ['test-artifact', 'test-artifact10', 'test-artifact11', 'test-artifact123'])

    @mock_s3
    def test_write_index(self):
        self._get_driver().write_index('test-artifact', '[{json: "message"}]')

    @mock_s3
    def test_write_index_unicode(self):
        self._get_driver().write_index('test-artifact', '[{json: "メッセージ"}]')

    @mock_s3
    def test_read_index(self):
        d = self._get_driver()
        d.write_index('test-artifact', '[{json: "message"}]')
        self.assertEqual(d.read_index('test-artifact'), '[{json: "message"}]')

    @mock_s3
    def test_read_index_unicode(self):
        d = self._get_driver()
        d.write_index('test-artifact', '[{json: "メッセージ"}]')
        self.assertEqual(d.read_index('test-artifact'), '[{json: "メッセージ"}]')

    @mock_s3
    def test_read_index_not_found(self):
        self.assertEqual(self._get_driver().read_index('test-artifact'), '')

    @mock_s3
    def test_upload(self):
        d = self._get_driver()
        d.upload('tests/resources/test-artifact-1.2.3.dat', 'a/b/c/test-artifact-1.2.3.dat',
                 '7a38cb250db7127113e00ad5e241d563')
        self.assertTrue(d.exists_object('a/b/c/test-artifact-1.2.3.dat'))
        self.assertEqual(d.bucket.Object('a/b/c/test-artifact-1.2.3.dat').e_tag.strip('"'),
                         '7a38cb250db7127113e00ad5e241d563')

        d.upload('tests/resources/test-artifact-1.2.3.dat', 'a/b/x/test-artifact-1.2.3.dat', None)
        self.assertTrue(d.exists_object('a/b/c/test-artifact-1.2.3.dat'))
        self.assertEqual(d.bucket.Object('a/b/c/test-artifact-1.2.3.dat').e_tag.strip('"'),
                         '7a38cb250db7127113e00ad5e241d563')

    @mock_s3
    def test_upload_md5_error(self):
        self.assertRaises(AssertionError, self._get_driver().upload, 'tests/resources/test-artifact-1.2.3.dat',
                          'a/b/c/test-artifact-1.2.3.dat', '7a')

    @mock_s3
    def test_download(self):
        d = self._get_driver()
        d.upload('tests/resources/test-artifact-1.2.3.dat', 'a/b/x/test-artifact-1.2.3.dat', None)

        # assert uploading
        self.assertTrue(d.exists_object('a/b/x/test-artifact-1.2.3.dat'))

        if os.path.exists(self.tmp_path):
            os.remove(self.tmp_path)
        self.assertFalse(os.path.exists(self.tmp_path))
        d.download('a/b/x/test-artifact-1.2.3.dat', self.tmp_path, '7a38cb250db7127113e00ad5e241d563')
        self.assertTrue(os.path.exists(self.tmp_path))
        os.remove(self.tmp_path)

    @mock_s3
    def test_download_not_found(self):
        self.assertRaises(ValueError, self._get_driver().download, 'a/b/c/test-artifact-1.2.3.dat', self.tmp_path, None)

    @mock_s3
    def test_download_md5_error(self):
        d = self._get_driver()
        d.upload('tests/resources/test-artifact-1.2.3.dat', 'a/b/x/test-artifact-1.2.3.dat', None)

        # assert uploading
        self.assertTrue(d.exists_object('a/b/x/test-artifact-1.2.3.dat'))

        self.assertFalse(os.path.exists(self.tmp_path))
        self.assertRaises(AssertionError, d.download, 'a/b/x/test-artifact-1.2.3.dat', self.tmp_path, '7a')
        self.assertFalse(os.path.exists(self.tmp_path))

    @mock_s3
    def test_delete(self):
        d = self._get_driver()
        d.upload('tests/resources/test-artifact-1.2.3.dat', 'a/b/x/test-artifact-1.2.3.dat', None)

        # assert uploading
        self.assertTrue(d.exists_object('a/b/x/test-artifact-1.2.3.dat'))

        d.delete('a/b/x/test-artifact-1.2.3.dat', '7a38cb250db7127113e00ad5e241d563')

        # assert key is deleted
        self.assertFalse(d.exists_object('a/b/x/test-artifact-1.2.3.dat'))

    @mock_s3
    def test_delete_not_found(self):
        self.assertRaises(ValueError, self._get_driver().delete, 'a/b/c/test-artifact-1.2.3.dat', None)

    @mock_s3
    def test_delete_md5_error(self):
        d = self._get_driver()
        d.upload('tests/resources/test-artifact-1.2.3.dat', 'a/b/x/test-artifact-1.2.3.dat', None)

        # assert uploading
        self.assertTrue(d.exists_object('a/b/x/test-artifact-1.2.3.dat'))

        self.assertRaises(AssertionError, d.delete, 'a/b/x/test-artifact-1.2.3.dat', '7a')

        # assert key is remained
        self.assertTrue(d.exists_object('a/b/x/test-artifact-1.2.3.dat'))

    @mock_s3
    def test_list_objects(self):
        d = self._get_driver()
        d.upload('tests/resources/test-artifact-1.2.3.dat', 'a/b/c/test-artifact-1.2.3.dat', None)
        d.upload('tests/resources/test-artifact-1.2.3.dat', 'a/b/x/test-artifact-1.2.3.dat', None)

        # assert uploading
        self.assertTrue(d.exists_object('a/b/c/test-artifact-1.2.3.dat'))
        self.assertTrue(d.exists_object('a/b/x/test-artifact-1.2.3.dat'))

        self.assertTrue(len(list(d.list_objects('a/b/c'))) is 1)
        self.assertTrue(len(list(d.list_objects('a/b/x'))) is 1)
        self.assertTrue(len(list(d.list_objects('a/b'))) is 2)

    @mock_s3
    def test_list_objects_non_exists_prefix(self):
        d = self._get_driver()
        self.assertTrue(len(list(d.list_objects('a/b/c'))) is 0)

    @mock_s3
    def test_exists_object(self):
        d = self._get_driver()

        self.assertFalse(d.exists_object('a/b/c/test-artifact-1.2.3.dat'))

        d.upload('tests/resources/test-artifact-1.2.3.dat', 'a/b/c/test-artifact-1.2.3.dat', None)

        self.assertTrue(d.exists_object('a/b/c/test-artifact-1.2.3.dat'))

    def test_s3_url(self):
        self.assertEqual(S3Driver.s3_url('bucket-name', 'a/b/c'), 's3://bucket-name/a/b/c')
