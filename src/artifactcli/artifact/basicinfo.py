import os
import re
from baseinfo import BaseInfo
from artifactcli.util import *


class BasicInfo(BaseInfo):
    keys = ['group_id', 'artifact_id', 'version', 'packaging', 'revision']

    def __init__(self, group_id, artifact_id, version, packaging, revision):
        super(BasicInfo, self).__init__(BasicInfo.keys)
        self.group_id = group_id
        self.artifact_id = artifact_id
        self.version = version
        self.packaging = packaging
        self.revision = revision

    def __str__(self):
        buf = [
            'Basic Info:',
            '  Group ID   : %s' % self.group_id,
            '  Artifact ID: %s' % self.artifact_id,
            '  Version    : %s' % self.version,
            '  Packaging  : %s' % self.packaging,
            '  Revision   : %s' % self.revision
        ]
        return to_str('\n'.join(buf))

    def filename(self):
        return '%s-%s.%s' % (self.artifact_id, self.version, self.packaging)

    def s3_path(self):
        if self.revision is None:
            raise ValueError('Revision is not defined')
        else:
            xs = (str(x) for x in [self.group_id, self.artifact_id, self.version, self.revision, self.filename()])
            return '/'.join(xs)

    @staticmethod
    def from_dict(d):
        return BasicInfo(*[d[k] for k in BasicInfo.keys])

    @staticmethod
    def from_path(group_id, path, revision=None):
        basename = os.path.basename(path)
        prefix, extension = os.path.splitext(basename)
        extension = extension[1:]  # remove dot
        tokens = reversed(prefix.split('-'))

        artifact_tokens = []
        version_tokens = []
        version_found = False
        for token in tokens:
            if version_found:
                artifact_tokens.append(token)
            else:
                version_tokens.append(token)
                if BasicInfo._is_version_like(token):
                    version_found = True

        artifact_id = '-'.join(reversed(artifact_tokens))
        version = '-'.join(reversed(version_tokens))

        # validate values
        if not version_found:
            raise ValueError('Could not parse version from path: %s' % path)
        if not artifact_id:
            raise ValueError('Could not parse artifact id from path: %s' % path)
        if not extension:
            raise ValueError('Could not parse extension from path: %s' % path)

        return BasicInfo(group_id, artifact_id, version, extension, revision)

    @staticmethod
    def _is_version_like(s):
        return re.match("^[0-9]+(?:[.][0-9]+)*$", s) is not None
