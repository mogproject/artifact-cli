import time
from datetime import datetime
import logging
import os
import dateutil.parser
import git
from baseinfo import BaseInfo
from artifactcli.util import *


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
            'Git Info:',
            '  Branch             : %s' % self.branch,
            '  Tags               : %s' % ', '.join(self.tags),
            '  Last Commit Author : %s <%s>' % (self.author_name, self.author_email),
            '  Last Commit Date   : %s' % self.committed_date,
            '  Last Commit Summary: %s' % self.summary,
            '  Last Commit SHA    : %s' % self.sha,
        ]
        return to_str('\n'.join(buf))

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
    def _search_git_repo(path):
        while True:
            try:
                return git.Repo(path)
            except git.InvalidGitRepositoryError:
                parent_dir = os.path.dirname(path)
                if path == parent_dir:
                    return None
                path = parent_dir
            except git.NoSuchPathError:
                return None

    @staticmethod
    def from_path(path):
        repo = GitInfo._search_git_repo(path)
        if not repo:
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
