from abc import ABCMeta, abstractmethod
from artifactcli.util import CaseClass


class BaseDriver(CaseClass):
    __metaclass__ = ABCMeta

    @abstractmethod
    def artifact_ids(self):
        """abstract method"""

    @abstractmethod
    def read_index(self, artifact_id):
        """abstract method"""

    @abstractmethod
    def write_index(self, artifact_id, s):
        """abstract method"""

    @abstractmethod
    def upload(self, local_path, remote_path, md5):
        """abstract method"""

    @abstractmethod
    def download(self, remote_path, local_path, md5):
        """abstract method"""

    @abstractmethod
    def delete(self, remote_path, md5):
        """abstract method"""
