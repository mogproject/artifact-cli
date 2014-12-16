import logging
from basedriver import BaseDriver


class MockDriver(BaseDriver):
    """
    Mock driver class
    """
    def __init__(self):
        super(MockDriver, self).__init__(['index_data', 'uploaded_data', 'downloaded_data'])
        self.index_data = ""
        self.uploaded_data = {}
        self.downloaded_data = {}

    def read_index(self):
        return self.index_data

    def write_index(self, s):
        self.index_data = s

    def upload(self, local_path, remote_path, md5):
        if md5 is None:
            md5 = 'example_md5'

        uploaded_md5 = md5
        self.uploaded_data[remote_path] = (local_path, uploaded_md5)

        assert md5 is None or md5 == uploaded_md5
        logging.info('[Mock] uploaded: %s -> %s' % (local_path, remote_path))

    def download(self, remote_path, local_path, md5):
        if remote_path not in self.uploaded_data:
            raise ValueError('File not found: %s' % remote_path)

        data, uploaded_md5 = self.uploaded_data[remote_path]
        self.downloaded_data[local_path] = (remote_path, uploaded_md5)

        assert md5 is None or md5 == uploaded_md5
        logging.info('[Mock] downloaded: %s -> %s' % (remote_path, local_path))
