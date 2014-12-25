from baseinfo import BaseInfo
from basicinfo import BasicInfo
from fileinfo import FileInfo
from gitinfo import GitInfo
from artifactcli.util import *


class Artifact(BaseInfo):
    keys = ['basic_info', 'file_info', 'scm_info']

    def __init__(self, basic_info, file_info, scm_info=None):
        super(Artifact, self).__init__(Artifact.keys)
        self.basic_info = basic_info
        self.file_info = file_info
        self.scm_info = scm_info

    def __str__(self):
        buf = [self.basic_info, self.file_info] + [self.scm_info] if self.scm_info else []
        return to_str('\n'.join(map(str, buf)))

    def to_dict(self):
        ret = {
            'basic_info': self.basic_info.to_dict(),
            'file_info': self.file_info.to_dict(),
        }
        if self.scm_info:
            ret.update({'scm_info': self.scm_info.to_dict()})
        return ret

    @staticmethod
    def from_dict(d):
        bi = BasicInfo.from_dict(d['basic_info'])
        fi = FileInfo.from_dict(d['file_info'])
        si = None
        if 'scm_info' in d:
            if d['scm_info']['system'] == 'git':
                si = GitInfo.from_dict(d['scm_info'])
        return Artifact(bi, fi, si)

    @staticmethod
    def from_path(group_id, path):
        # revision will be set to None
        return Artifact(BasicInfo.from_path(group_id, path), FileInfo.from_path(path), GitInfo.from_path(path))
