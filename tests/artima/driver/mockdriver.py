from src.artima.driver import BaseDriver


class MockDriver(BaseDriver):
    """
    Mock driver class
    """
    def __init__(self):
        self.index_data = ""
        self.uploaded_data = {}

    def read_index(self):
        return self.index_data

    def write_index(self, s):
        self.index_data = s

    def upload(self, local_path, remote_path, md5=None):
        if md5 is None:
            md5 = 'example_md5'

        uploaded_md5 = md5
        self.uploaded_data[remote_path] = (local_path, uploaded_md5)

        assert md5 is None or md5 == uploaded_md5
        print('[Mock] uploaded: %s -> %s' % (local_path, remote_path))

    def download(self, remote_path, local_path, md5=None):
        if not remote_path in self.uploaded_data:
            raise KeyError('File not found: %s' % remote_path)

        data, uploaded_md5 = self.uploaded_data[remote_path]
        assert md5 is None or md5 == uploaded_md5
        print('[Mock] downloaded: %s -> %s' % (remote_path, local_path))

