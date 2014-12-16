import os
import time
import socket
import getpass
from datetime import datetime
import dateutil.parser


class FileInfo(object):
    keys = ['host', 'user', 'size', 'mtime', 'md5']

    def __init__(self, host, user, size, mtime, md5):
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
            '  Size    : %s (%s)' % (self.size, FileInfo.sizeof_fmt(self.size)),
            '  MD5     : %s' % self.md5,
        ]
        return '\n'.join(buf)

    def __repr__(self):
        return 'FileInfo(host=%s, user=%s, size=%s, mtime=%s, md5=%s)' % (
            self.host, self.user, self.size, self.mtime, self.md5)

    def __eq__(self, other):
        return isinstance(other, FileInfo) and all(getattr(self, k) == getattr(other, k) for k in FileInfo.keys)

    def __ne__(self, other):
        return not self == other

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

    @staticmethod
    def sizeof_fmt(num, suffix='B'):
        for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
            if abs(num) < 1024.0:
                return "%3.1f%s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f%s%s" % (num, 'Yi', suffix)