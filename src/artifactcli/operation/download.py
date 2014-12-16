from baseoperation import BaseOperation


class DownloadOperation(BaseOperation):
    def __init__(self, group_id, args, print_only):
        super(DownloadOperation, self).__init__(group_id, args, {'print_only': print_only})
        self.local_path = self._get_arg(0, 'LOCAL_PATH')
        self.revision = self._get_arg(1, 'REVISION')
        assert self.revision.isdigit() or self.revision == 'latest'

    def run(self, repo):
        revision = None if self.revision == 'latest' else int(self.revision)
        repo.load()
        repo.download(self.group_id, self.local_path, revision, print_only=self.print_only)
        return 0
