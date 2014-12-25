import os
import time
import socket
import getpass
from datetime import datetime
import dateutil.parser
from baseinfo import BaseInfo
from artifactcli.util import *


class FileInfo(BaseInfo):
    keys = ['host', 'user', 'size', 'mtime', 'md5']

    def __init__(self, host, user, size, mtime, md5):
        super(FileInfo, self).__init__(FileInfo.keys)
        self.host = host
        self.user = user
        self.size = size
        self.mtime = mtime
        self.md5 = md5

    def __str__(self):
        buf = [
            'File Info:',
            '  User    : %s@%s' % (self.user, self.host),
            '  Modified: %s' % self.mtime,
            '  Size    : %s (%s)' % (self.size, self.size_format()),
            '  MD5     : %s' % self.md5,
        ]
        return to_str('\n'.join(buf))

    def to_dict(self):
        return {
            'host': self.host,
            'user': self.user,
            'size': self.size,
            'mtime': self.mtime.isoformat(),
            'hex_md5': self.md5
        }

    @staticmethod
    def from_path(path):
        host = socket.gethostname()
        user = getpass.getuser()
        size = os.path.getsize(path)
        mtime = datetime(*time.localtime(os.path.getmtime(path))[:6])
        md5 = FileInfo.get_hex_md5(path)
        return FileInfo(host, user, size, mtime, md5)

    @staticmethod
    def from_dict(d):
        return FileInfo(d['host'], d['user'], d['size'], dateutil.parser.parse(d['mtime']), d['hex_md5'])

    @staticmethod
    def get_hex_md5(path):
        import hashlib

        hasher = hashlib.md5()
        blocksize = 65536
        with open(path, 'rb') as f:
            buf = f.read(blocksize)
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(blocksize)
        return hasher.hexdigest()

    def size_format(self):
        return self._sizeof_fmt(self.size)

    @classmethod
    def _sizeof_fmt(cls, num, suffix='B'):
        for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
            if abs(num) < 1024.0:
                return "%3.1f%s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f%s%s" % (num, 'Yi', suffix)
