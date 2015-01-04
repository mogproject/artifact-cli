import logging
import boto
import boto.s3
from boto.s3.key import Key
from boto.s3.connection import OrdinaryCallingFormat
from basedriver import BaseDriver
from artifactcli.util import assert_type

DEFAULT_REGION = 'us-east-1'
DEFAULT_INDEX_NAME = 'artifact-cli-index.json'


class S3Driver(BaseDriver):
    """
    S3 driver class
    """

    def __init__(self, aws_access_key, aws_secret_key, bucket_name, group_id,
                 region=None, index_name=None, connection=None):
        super(S3Driver, self).__init__(['aws_access_key', 'aws_secret_key', 'bucket_name', 'region', 'index_path'])
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.bucket_name = bucket_name
        self.region = region or DEFAULT_REGION
        self.index_path = '%s/%s' % (group_id, (index_name or DEFAULT_INDEX_NAME))
        self.__conn = connection
        self.__bucket = None

    def connect(self):
        self.__conn = self.__conn or boto.s3.connect_to_region(
            self.region,
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key,
            is_secure=True)
        self.__bucket = self.__conn.get_bucket(self.bucket_name)

    def bucket(self):
        if not self.__bucket:
            self.connect()
        return self.__bucket

    def read_index(self):
        """
        Read index data from S3 bucket.

        :return: index json text in unicode
        """
        logging.info('Reading index: %s' % self.s3_url(self.bucket_name, self.index_path))
        k = self.bucket().get_key(self.index_path)
        if k:
            s = k.get_contents_as_string(encoding='utf-8')
        else:
            s = u''

        return assert_type(s, unicode)

    def write_index(self, s):
        """
        Write index data to S3 bucket.

        :param s: index json text in unicode
        :return: None
        """
        assert_type(s, unicode)

        logging.info('Writing index: %s' % self.s3_url(self.bucket_name, self.index_path))
        k = Key(self.bucket())
        k.key = self.index_path
        k.set_metadata('Content-Type', 'application/json; charset=utf-8')
        k.set_contents_from_string(s.encode('utf-8'))

    def upload(self, local_path, remote_path, md5):
        """
        Upload local file to S3 bucket.
        File will be overwritten when already exists.

        :param local_path: source file path
        :param remote_path: S3 path to upload
        :param md5: MD5 digest hex string to verify
        :return None
        """
        k = Key(self.bucket())
        k.key = remote_path
        logging.info('Uploading file: %s' % self.s3_url(self.bucket_name, remote_path))
        k.set_contents_from_filename(local_path)
        remote_md5 = self.bucket().get_key(remote_path).etag.strip('"')
        assert md5 is None or md5 == remote_md5, \
            'Failed to check MD5 digest: local=%s, remote=%s' % (md5, remote_md5)

    def download(self, remote_path, local_path, md5):
        """
        Download file from S3 bucket.

        :param remote_path: S3 path to download
        :param local_path: local destination path
        :param md5: MD5 digest hex string to verify
        :return: None
        """
        k = self.bucket().get_key(remote_path)
        if not k:
            raise ValueError('File not found: %s' % self.s3_url(self.bucket(), remote_path))
        remote_md5 = k.etag.strip('"')
        assert md5 is None or md5 == remote_md5, \
            'Failed to check MD5 digest: local=%s, remote=%s' % (md5, remote_md5)

        k.get_contents_to_filename(local_path)
        logging.info('Downloaded: %s' % local_path)

    def delete(self, remote_path, md5):
        """
        Delete file from S3 bucket.

        :param remote_path: S3 path to delete
        :param md5: MD5 digest hex string to verify
        :return: None
        """
        k = self.bucket().get_key(remote_path)
        if not k:
            raise ValueError('File not found: %s' % self.s3_url(self.bucket(), remote_path))
        remote_md5 = k.etag.strip('"')
        assert md5 is None or md5 == remote_md5, \
            'Failed to check MD5 digest: local=%s, remote=%s' % (md5, remote_md5)

        k.delete()
        logging.info('Deleted: %s' % remote_path)

    @classmethod
    def s3_url(cls, bucket_name, key):
        return 's3://%s/%s' % (bucket_name, key)
