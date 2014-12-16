from .basicinfo import BasicInfo
from .fileinfo import FileInfo
from .gitinfo import GitInfo


class Artifact(object):
    keys = ['basic_info', 'file_info', 'scm_info']

    def __init__(self, basic_info, file_info, scm_info=None):
        self.basic_info = basic_info
        self.file_info = file_info
        self.scm_info = scm_info

    def __str__(self):
        buf = [
            '%s' % self.basic_info,
            '%s' % self.file_info,
            '%s' % self.scm_info
        ]
        return '\n'.join(buf)

    def __repr__(self):
        return 'Artifact(basic_info=%s, file_info=%s, scm_info=%s)' % (
            repr(self.basic_info), repr(self.file_info), repr(self.scm_info))

    def __eq__(self, other):
        return isinstance(other, Artifact) and all(getattr(self, k) == getattr(other, k) for k in Artifact.keys)

    def __ne__(self, other):
        return not self == other

    def to_dict(self):
        return {
            'basic_info': self.basic_info.to_dict(),
            'file_info': self.file_info.to_dict(),
            'scm_info': self.scm_info.to_dict(),
        }

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

