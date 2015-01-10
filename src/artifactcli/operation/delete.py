import logging
from baseoperation import BaseOperation
from artifactcli.artifact import BasicInfo


class DeleteOperation(BaseOperation):
    def __init__(self, group_id, args, print_only):
        super(DeleteOperation, self).__init__(group_id, args, {'print_only': print_only})
        self.file_name = self._get_arg(0, 'FILE_NAME')
        self.revision = self._get_arg(1, 'REVISION')
        assert self.revision.isdigit()

    def run(self, repo):
        revision = int(self.revision)

        try:
            artifact_id = BasicInfo.from_path(self.group_id, self.file_name).artifact_id
            repo.load(artifact_id)
            repo.delete(self.file_name, revision, print_only=self.print_only)
            repo.save(artifact_id)
        except ValueError as e:
            logging.warn(e)
            return 2

        return 0
