import time
from datetime import datetime
import dateutil.parser
import git


class GitInfo(object):
    keys = ['branch', 'tags', 'author_name', 'author_email', 'committed_date', 'summary']

    def __init__(self, branch, tags, author_name, author_email, committed_date, summary, sha):
        self.system = 'git'
        self.branch = branch
        self.tags = tags
        self.author_name = author_name
        self.author_email = author_email
        self.committed_date = committed_date
        self.summary = summary
        self.sha = sha

    def __str__(self):
        buf = [
            'Git Info:',
            '  Branch             : %s' % self.branch,
            '  Tags               : %s' % self.tags,
            '  Last Commit Author : %s <%s>' % (self.author_name, self.author_email),
            '  Last Commit Date   : %s' % self.committed_date,
            '  Last Commit Summary: %s' % self.summary,
            '  Last Commit SHA    : %s' % self.sha,
        ]
        return '\n'.join(buf)

    def __repr__(self):
        s = 'GitInfo(branch=%s, tags=%s, author_name=%s, author_email=%s, committed_date=%s, summary=%s, sha=%s)'
        return s % (
            self.branch, self.tags, self.author_name, self.author_email, self.committed_date, self.summary, self.sha)

    def __eq__(self, other):
        return isinstance(other, GitInfo) and all(getattr(self, k) == getattr(other, k) for k in GitInfo.keys)

    def __ne__(self, other):
        return not self == other

    def to_dict(self):
        return {
            'system': self.system,
            'branch': self.branch,
            'tags': self.tags,
            'author_name': self.author_name,
            'author_email': self.author_email,
            'committed_date': self.committed_date.isoformat(),
            'summary': self.summary,
            'sha': self.sha,
        }

    @staticmethod
    def from_dict(d):
        return GitInfo(
            d['branch'],
            d['tags'],
            d['author_name'],
            d['author_email'],
            dateutil.parser.parse(d['committed_date']),
            d['summary'],
            d['sha'],
        )

    @staticmethod
    def from_path(path):
        repo = git.Repo(path)
        ref = repo.head.reference
        branch = ref.name
        author_name = ref.commit.author.name
        author_email = ref.commit.author.email
        summary = ref.commit.summary
        sha = ref.commit.hexsha
        epoch = ref.commit.committed_date
        committed_date = datetime(*time.localtime(epoch)[:6])
        tags = [t.name for t in repo.tags if t.commit.hexsha == sha]
        return GitInfo(branch, tags, author_name, author_email, committed_date, summary, sha)
