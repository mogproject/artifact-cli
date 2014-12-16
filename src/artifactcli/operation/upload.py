from baseoperation import BaseOperation


class UploadOperation(BaseOperation):
    def __init__(self, group_id, args, force, print_only):
        super(UploadOperation, self).__init__(group_id, args, {'force': force, 'print_only': print_only})
        self.local_path = self._get_arg(0, 'LOCAL_PATH')

    def run(self, repo):
        repo.load()
        repo.upload(self.group_id, self.local_path, force=self.force, print_only=self.print_only)
        return 0
