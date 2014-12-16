import unittest
import os
import boto
from moto import mock_s3
from artifactcli.driver import S3Driver


class TestS3Driver(unittest.TestCase):
    def setUp(self):
        self.tmp_path = 'tests/resources/test-artifact-1.2.3.dat.tmp'

    @mock_s3
    def test_write_index_and_read_index(self):
        boto.connect_s3('XXX', 'YYY').create_bucket('bucket4art')
        d = S3Driver('XXX', 'YYY', 'bucket4art', 'gid')
        d.write_index('[{json: "message"}]')

    @mock_s3
    def test_read_index(self):
        boto.connect_s3('XXX', 'YYY').create_bucket('bucket4art')
        d = S3Driver('XXX', 'YYY', 'bucket4art', 'gid')
        d.write_index('[{json: "message"}]')
        self.assertEqual(d.read_index(), '[{json: "message"}]')

    @mock_s3
    def test_read_index_not_found(self):
        boto.connect_s3('XXX', 'YYY').create_bucket('bucket4art')
        d = S3Driver('XXX', 'YYY', 'bucket4art', 'gid')
        self.assertEqual(d.read_index(), '')

    @mock_s3
    def test_upload(self):
        boto.connect_s3('XXX', 'YYY').create_bucket('bucket4art')
        d = S3Driver('XXX', 'YYY', 'bucket4art', 'gid')
        d.upload('tests/resources/test-artifact-1.2.3.dat', 'a/b/c/test-artifact-1.2.3.dat',
                 '7a38cb250db7127113e00ad5e241d563')
        d.upload('tests/resources/test-artifact-1.2.3.dat', 'a/b/x/test-artifact-1.2.3.dat', None)

    @mock_s3
    def test_upload_md5_error(self):
        boto.connect_s3('XXX', 'YYY').create_bucket('bucket4art')
        d = S3Driver('XXX', 'YYY', 'bucket4art', 'gid')
        self.assertRaises(AssertionError, d.upload, 'tests/resources/test-artifact-1.2.3.dat',
                          'a/b/c/test-artifact-1.2.3.dat', '7a')

    @mock_s3
    def test_download(self):
        boto.connect_s3('XXX', 'YYY').create_bucket('bucket4art')
        d = S3Driver('XXX', 'YYY', 'bucket4art', 'gid')
        d.upload('tests/resources/test-artifact-1.2.3.dat', 'a/b/x/test-artifact-1.2.3.dat', None)

        if os.path.exists(self.tmp_path):
            os.remove(self.tmp_path)
        self.assertFalse(os.path.exists(self.tmp_path))
        d.download('a/b/x/test-artifact-1.2.3.dat', self.tmp_path, '7a38cb250db7127113e00ad5e241d563')
        self.assertTrue(os.path.exists(self.tmp_path))
        os.remove(self.tmp_path)

    @mock_s3
    def test_download_not_found(self):
        boto.connect_s3('XXX', 'YYY').create_bucket('bucket4art')
        d = S3Driver('XXX', 'YYY', 'bucket4art', 'gid')
        self.assertRaises(ValueError, d.download, 'a/b/c/test-artifact-1.2.3.dat', self.tmp_path, None)

    @mock_s3
    def test_download_md5_error(self):
        boto.connect_s3('XXX', 'YYY').create_bucket('bucket4art')
        d = S3Driver('XXX', 'YYY', 'bucket4art', 'gid')
        d.upload('tests/resources/test-artifact-1.2.3.dat', 'a/b/x/test-artifact-1.2.3.dat', None)

        self.assertFalse(os.path.exists(self.tmp_path))
        self.assertRaises(AssertionError, d.download, 'a/b/x/test-artifact-1.2.3.dat', self.tmp_path, '7a')
        self.assertFalse(os.path.exists(self.tmp_path))

    def test_s3_url(self):
        self.assertEqual(S3Driver.s3_url('bucket-name', 'a/b/c'), 's3://bucket-name/a/b/c')
