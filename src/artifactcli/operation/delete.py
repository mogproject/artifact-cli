from baseoperation import BaseOperation


class DeleteOperation(BaseOperation):
    def __init__(self, group_id, args, print_only):
        super(DeleteOperation, self).__init__(group_id, args, {'print_only': print_only})
        self.file_name = self._get_arg(0, 'FILE_NAME')
        self.revision = self._get_arg(1, 'REVISION')
        assert self.revision.isdigit()

    def run(self, repo):
        revision = int(self.revision)
        repo.load()
        repo.delete(self.group_id, self.file_name, revision, print_only=self.print_only)
        return 0
