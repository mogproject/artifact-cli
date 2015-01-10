import logging
from baseoperation import BaseOperation
from artifactcli import BasicInfo


class InfoOperation(BaseOperation):
    def __init__(self, group_id, args, output=None):
        super(InfoOperation, self).__init__(group_id, args, {'output': output})
        self.file_name = self._get_arg(0, 'FILE_NAME')
        self.revision = self._get_arg(1, 'REVISION')
        assert self.revision.isdigit() or self.revision == 'latest'

    def run(self, repo):
        revision = None if self.revision == 'latest' else int(self.revision)

        try:
            repo.load(BasicInfo.from_path(self.group_id, self.file_name).artifact_id)
            repo.print_info(self.file_name, revision, self.output)
        except ValueError as e:
            logging.warn(e)
            return 2

        return 0
