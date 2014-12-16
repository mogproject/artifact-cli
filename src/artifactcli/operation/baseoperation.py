import logging
from abc import ABCMeta, abstractmethod
from artifactcli.util.caseclass import CaseClass


class BaseOperation(CaseClass):
    __metaclass__ = ABCMeta

    def __init__(self, group_id=None, args=None, optional_params=None):
        optional_params = optional_params or {}
        super(BaseOperation, self).__init__(['group_id', 'args'] + optional_params.keys())

        self.group_id = group_id
        self.args = args

        for k in optional_params:
            setattr(self, k, optional_params[k])

    def _get_arg(self, index, name):
        try:
            return self.args[index]
        except IndexError:
            logging.error('Argument <%s> is required.' % name)
            raise AssertionError

    @abstractmethod
    def run(self, repo):
        """abstract method"""
