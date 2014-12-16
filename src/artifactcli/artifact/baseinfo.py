from artifactcli.util import CaseClass


class BaseInfo(CaseClass):
    def to_dict(self):
        return dict((k, getattr(self, k)) for k in self.keys)
