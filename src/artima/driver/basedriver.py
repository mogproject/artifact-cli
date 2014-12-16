from abc import ABCMeta, abstractmethod


class BaseDriver(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def read_index(self):
        pass

    @abstractmethod
    def write_index(self, s):
        pass

    @abstractmethod
    def upload(self, local_path, remote_path, md5=None):
        pass

    @abstractmethod
    def download(self, remote_path, local_path, md5=None):
        pass
