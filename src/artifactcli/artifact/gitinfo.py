import time
from datetime import datetime
import logging
import dateutil.parser
import git
from baseinfo import BaseInfo
from artifactcli.util import assert_type


class GitInfo(BaseInfo):
    keys = ['branch', 'tags', 'author_name', 'author_email', 'committed_date', 'summary', 'sha']

    def __init__(self, branch, tags, author_name, author_email, committed_date, summary, sha):
        super(GitInfo, self).__init__(GitInfo.keys)
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
            u'Git Info:',
            u'  Branch             : %s' % self.branch,
            u'  Tags               : %s' % ', '.join(self.tags),
            u'  Last Commit Author : %s <%s>' % (self.author_name, self.author_email),
            u'  Last Commit Date   : %s' % self.committed_date,
            u'  Last Commit Summary: %s' % self.summary,
            u'  Last Commit SHA    : %s' % self.sha,
        ]
        return assert_type(u'\n'.join(buf).encode('utf-8'), str)

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
        try:
            repo = git.Repo(path)
        except (git.InvalidGitRepositoryError, git.NoSuchPathError):
            logging.warn('Failed to fetch Git information: %s' % path)
            return None

        try:
            ref = repo.head.reference
        except TypeError:
            logging.warn('Failed to get Git HEAD reference: %s' % path)
            ref = repo.head

        branch = '' if ref.name == 'HEAD' else ref.name
        author_name = ref.commit.author.name
        author_email = ref.commit.author.email
        summary = ref.commit.summary
        sha = ref.commit.hexsha
        epoch = ref.commit.committed_date
        committed_date = datetime(*time.localtime(epoch)[:6])
        tags = [t.name for t in repo.tags if t.commit.hexsha == sha]
        return GitInfo(branch, tags, author_name, author_email, committed_date, summary, sha)
