import logging
import re
import boto3
from botocore.exceptions import ClientError
from .basedriver import BaseDriver
from artifactcli.util import assert_type, ProgressBar

DEFAULT_REGION = 'us-east-1'
DEFAULT_INDEX_PREFIX = '.meta/index-'


class S3Driver(BaseDriver):
    """
    S3 driver class
    """

    def __init__(self, aws_access_key, aws_secret_key, bucket_name, group_id,
                 region=None, index_prefix=None, session=None):
        super(S3Driver, self).__init__(['aws_access_key', 'bucket_name', 'region', 'index_prefix'])
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.bucket_name = bucket_name
        self.region = region or DEFAULT_REGION
        self.index_prefix = '%s/%s' % (group_id, index_prefix or DEFAULT_INDEX_PREFIX)
        self.session = session or boto3.session.Session(
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key,
            region_name=self.region)
        self.bucket = self.session.resource('s3').Bucket(self.bucket_name)

    def index_path(self, artifact_id):
        return '%s%s.json' % (self.index_prefix, artifact_id)

    def artifact_ids(self):
        """
        Get list of the artifact IDs in the directory

        :return: sorted list of artifact IDs
        """
        keys = [obj['Key'][len(self.index_prefix):] for obj in self.list_objects(self.index_prefix)]
        results = [re.search('(.*)[.]json', k) for k in keys]
        return sorted(r.group(1) for r in results if r)

    def read_index(self, artifact_id):
        """
        Read index data from S3 bucket.

        :param artifact_id: artifact id to read
        :return: index json text in unicode
        """
        index_path = self.index_path(artifact_id)
        logging.debug('Reading index: %s' % self.s3_url(self.bucket_name, index_path))
        if self.exists_object(index_path):
            s = self.bucket.Object(index_path).get()['Body'].read().decode('utf-8')
        else:
            s = str()

        return s

    def write_index(self, artifact_id, s):
        """
        Write index data to S3 bucket.

        :param artifact_id: artifact id to write
        :param s: index json text in unicode
        :return: None
        """
        index_path = self.index_path(artifact_id)
        logging.debug('Writing index: %s' % self.s3_url(self.bucket_name, index_path))
        self.bucket.Object(index_path).put(Body=s.encode('utf-8'), ContentType='application/json; charset=utf-8')

    def upload(self, local_path, remote_path, md5):
        """
        Upload local file to S3 bucket.
        File will be overwritten when already exists.

        :param local_path: source file path
        :param remote_path: S3 path to upload
        :param md5: MD5 digest hex string to verify
        :return None
        """
        with ProgressBar():
            self.bucket.Object(remote_path).upload_file(Filename=local_path)

        remote_md5 = self.bucket.Object(remote_path).e_tag.strip('"')
        assert md5 is None or md5 == remote_md5, \
            'Failed to check MD5 digest: local=%s, remote=%s' % (md5, remote_md5)

        logging.info('Uploaded: %s' % self.s3_url(self.bucket_name, remote_path))

    def download(self, remote_path, local_path, md5):
        """
        Download file from S3 bucket.

        :param remote_path: S3 path to download
        :param local_path: local destination path
        :param md5: MD5 digest hex string to verify
        :return: None
        """
        if not self.exists_object(remote_path):
            raise ValueError('File not found: %s' % self.s3_url(self.bucket_name, remote_path))
        obj = self.bucket.Object(remote_path)
        remote_md5 = obj.e_tag.strip('"')
        assert md5 is None or md5 == remote_md5, \
            'Failed to check MD5 digest: local=%s, remote=%s' % (md5, remote_md5)

        with ProgressBar():
            obj.download_file(Filename=local_path)

        logging.info('Downloaded: %s' % local_path)

    def delete(self, remote_path, md5):
        """
        Delete file from S3 bucket.

        :param remote_path: S3 path to delete
        :param md5: MD5 digest hex string to verify
        :return: None
        """
        if not self.exists_object(remote_path):
            raise ValueError('File not found: %s' % self.s3_url(self.bucket_name, remote_path))
        obj = self.bucket.Object(remote_path)
        remote_md5 = obj.e_tag.strip('"')
        assert md5 is None or md5 == remote_md5, \
            'Failed to check MD5 digest: local=%s, remote=%s' % (md5, remote_md5)

        obj.delete()
        logging.info('Deleted: %s' % remote_path)

    def list_objects(self, prefix):
        client = self.session.client('s3')
        continuation_token = None
        while True:
            if continuation_token is None:
                res = client.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix)
            else:
                res = client.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix,
                                             ContinuationToken=continuation_token)

            if 'Contents' in res:
                yield from res['Contents']
            else:
                break

            if res['IsTruncated']:
                continuation_token = res['NextContinuationToken']
            else:
                break

    def exists_object(self, key):
        try:
            self.bucket.Object(key).get()
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                return False
            else:
                raise
        return True

    @classmethod
    def s3_url(cls, bucket_name, key):
        return 's3://%s/%s' % (bucket_name, key)
