from baseoperation import BaseOperation


class HelpOperation(BaseOperation):
    def __init__(self, parser):
        super(HelpOperation, self).__init__()
        self.parser = parser

    def run(self, repo=None):
        self.parser.print_help()
        return 1
