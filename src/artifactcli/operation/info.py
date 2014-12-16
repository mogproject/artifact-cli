import logging
from baseoperation import BaseOperation


class InfoOperation(BaseOperation):
    def __init__(self, group_id, args, output=None):
        super(InfoOperation, self).__init__(group_id, args, {'output': output})
        self.file_name = self._get_arg(0, 'FILE_NAME')
        self.revision = self._get_arg(1, 'REVISION')
        assert self.revision.isdigit() or self.revision == 'latest'

    def run(self, repo):
        revision = None if self.revision == 'latest' else int(self.revision)

        # suppress logging
        logging.getLogger().disabled = True
        repo.load()
        logging.getLogger().disabled = False

        try:
            repo.print_info(self.group_id, self.file_name, revision, self.output)
        except ValueError as e:
            logging.warn(e)
            return 2

        return 0
