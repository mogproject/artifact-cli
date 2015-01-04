# -*- encoding: utf-8 -*-

import unittest
import os
import boto
from moto import mock_s3
from artifactcli.driver import S3Driver


class TestS3Driver(unittest.TestCase):
    def setUp(self):
        self.tmp_path = 'tests/resources/test-artifact-1.2.3.dat.tmp'

    def _get_driver(self):
        conn = boto.connect_s3('XXX', 'YYY')
        boto.connect_s3('XXX', 'YYY').create_bucket('bucket4art')
        return S3Driver('XXX', 'YYY', 'bucket4art', 'gid', connection=conn)

    @mock_s3
    def test_write_index(self):
        self._get_driver().write_index(u'[{json: "message"}]')

    @mock_s3
    def test_write_index_unicode(self):
        self._get_driver().write_index(u'[{json: "メッセージ"}]')

    @mock_s3
    def test_read_index(self):
        d = self._get_driver()
        d.write_index(u'[{json: "message"}]')
        self.assertEqual(d.read_index(), u'[{json: "message"}]')

    @mock_s3
    def test_read_index_unicode(self):
        d = self._get_driver()
        d.write_index(u'[{json: "メッセージ"}]')
        self.assertEqual(d.read_index(), u'[{json: "メッセージ"}]')

    @mock_s3
    def test_read_index_not_found(self):
        self.assertEqual(self._get_driver().read_index(), '')

    @mock_s3
    def test_upload(self):
        d = self._get_driver()
        d.upload('tests/resources/test-artifact-1.2.3.dat', 'a/b/c/test-artifact-1.2.3.dat',
                 '7a38cb250db7127113e00ad5e241d563')
        self.assertFalse(d.bucket().get_key('a/b/c/test-artifact-1.2.3.dat') is None)
        self.assertEqual(d.bucket().get_key('a/b/c/test-artifact-1.2.3.dat').etag.strip('"'),
                         '7a38cb250db7127113e00ad5e241d563')

        d.upload('tests/resources/test-artifact-1.2.3.dat', 'a/b/x/test-artifact-1.2.3.dat', None)
        self.assertFalse(d.bucket().get_key('a/b/x/test-artifact-1.2.3.dat') is None)
        self.assertEqual(d.bucket().get_key('a/b/x/test-artifact-1.2.3.dat').etag.strip('"'),
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
        self.assertFalse(d.bucket().get_key('a/b/x/test-artifact-1.2.3.dat') is None)

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
        self.assertFalse(d.bucket().get_key('a/b/x/test-artifact-1.2.3.dat') is None)

        self.assertFalse(os.path.exists(self.tmp_path))
        self.assertRaises(AssertionError, d.download, 'a/b/x/test-artifact-1.2.3.dat', self.tmp_path, '7a')
        self.assertFalse(os.path.exists(self.tmp_path))

    @mock_s3
    def test_delete(self):
        d = self._get_driver()
        d.upload('tests/resources/test-artifact-1.2.3.dat', 'a/b/x/test-artifact-1.2.3.dat', None)

        # assert uploading
        self.assertFalse(d.bucket().get_key('a/b/x/test-artifact-1.2.3.dat') is None)

        d.delete('a/b/x/test-artifact-1.2.3.dat', '7a38cb250db7127113e00ad5e241d563')

        # assert key is deleted
        self.assertTrue(d.bucket().get_key('a/b/x/test-artifact-1.2.3.dat') is None)

    @mock_s3
    def test_delete_not_found(self):
        self.assertRaises(ValueError, self._get_driver().delete, 'a/b/c/test-artifact-1.2.3.dat', None)

    @mock_s3
    def test_delete_md5_error(self):
        d = self._get_driver()
        d.upload('tests/resources/test-artifact-1.2.3.dat', 'a/b/x/test-artifact-1.2.3.dat', None)

        # assert uploading
        self.assertFalse(d.bucket().get_key('a/b/x/test-artifact-1.2.3.dat') is None)

        self.assertRaises(AssertionError, d.delete, 'a/b/x/test-artifact-1.2.3.dat', '7a')

        # assert key is remained
        self.assertFalse(d.bucket().get_key('a/b/x/test-artifact-1.2.3.dat') is None)

    def test_s3_url(self):
        self.assertEqual(S3Driver.s3_url('bucket-name', 'a/b/c'), 's3://bucket-name/a/b/c')
