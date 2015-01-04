import logging
from basedriver import BaseDriver
from artifactcli.util import assert_type


class MockDriver(BaseDriver):
    """
    Mock driver class
    """

    def __init__(self):
        super(MockDriver, self).__init__(['index_data', 'uploaded_data', 'downloaded_data'])
        self.index_data = u''
        self.uploaded_data = {}
        self.downloaded_data = {}

    def read_index(self):
        """
        :return: index json text in unicode
        """
        return assert_type(self.index_data.decode('utf-8'), unicode)

    def write_index(self, s):
        """
        :param s: index json text in unicode
        :return: None
        """
        assert_type(s, unicode)
        self.index_data = s.encode('utf-8')

    def upload(self, local_path, remote_path, md5):
        if md5 is None:
            md5 = 'example_md5'

        uploaded_md5 = md5
        assert md5 is None or md5 == uploaded_md5

        self.uploaded_data[remote_path] = (local_path, uploaded_md5)
        logging.info('[Mock] uploaded: %s -> %s' % (local_path, remote_path))

    def download(self, remote_path, local_path, md5):
        if remote_path not in self.uploaded_data:
            raise ValueError('File not found: %s' % remote_path)

        data, uploaded_md5 = self.uploaded_data[remote_path]
        assert md5 is None or md5 == uploaded_md5

        self.downloaded_data[local_path] = (remote_path, uploaded_md5)
        logging.info('[Mock] downloaded: %s -> %s' % (remote_path, local_path))

    def delete(self, remote_path, md5):
        if remote_path not in self.uploaded_data:
            raise ValueError('File not found: %s' % remote_path)

        data, uploaded_md5 = self.uploaded_data[remote_path]
        assert md5 is None or md5 == uploaded_md5

        del self.uploaded_data[remote_path]
        logging.info('[Mock] deleted: %s' % remote_path)
