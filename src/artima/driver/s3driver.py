from boto.s3.connection import S3Connection
from boto.s3.key import Key
from basedriver import BaseDriver

DEFAULT_INDEX_PATH = 'artima-index'
S3_HOST = 's3-ap-northeast-1.amazonaws.com'


class S3Driver(BaseDriver):
    """
    S3 driver class
    """
    def __init__(self, aws_access_key, aws_secret_key, bucket_name, index_path=DEFAULT_INDEX_PATH):
        self.conn = S3Connection(aws_access_key, aws_secret_key, host=S3_HOST)
        self.bucket_name = bucket_name
        self.bucket = self.conn.get_bucket(bucket_name)
        self.index_path = index_path

    def read_index(self):
        """
        Read index data from S3 bucket.
        :return: index data as string
        """
        print('Reading index data: %s' % self.s3_url(self.bucket_name, self.index_path))
        k = self.bucket.get_key(self.index_path)
        if k:
            s = k.get_contents_as_string()
        else:
            s = ''
        return s

    def write_index(self, s):
        """
        Write index data to S3 bucket.
        :param s: index data in string
        :return: None
        """
        print('Writing index data: %s' % self.s3_url(self.bucket_name, self.index_path))
        k = Key(self.bucket)
        k.key = self.index_path
        k.set_contents_from_string(s)

    def upload(self, local_path, remote_path, md5=None):
        """
        Upload local file to S3 bucket.
        File will be overwritten when already exists.

        :param local_path: source file path
        :param remote_path: S3 path to upload
        :param md5: MD5 digest hex string to verify
        :return None
        """
        k = Key(self.bucket)
        k.key = remote_path
        print('Uploading file: %s' % self.s3_url(self.bucket_name, remote_path))
        k.set_contents_from_filename(local_path)
        assert md5 is None or md5 == self.bucket.get_key(remote_path).md5

    def download(self, remote_path, local_path, md5=None):
        """
        Download file from S3 bucket.
        :param remote_path: S3 path to download
        :param local_path: local destination path
        :param md5: MD5 digest hex string to verify
        :return: None
        """
        k = self.bucket.get_key(remote_path)
        if not k:
            raise KeyError('File not found: %s' % self.s3_url(self.bucket, remote_path))
        assert md5 is None or md5 == k.md5

        k.get_contents_to_filename(local_path)

    @classmethod
    def s3_url(cls, bucket_name, key):
        return 's3://%s/%s' % (bucket_name, key)
