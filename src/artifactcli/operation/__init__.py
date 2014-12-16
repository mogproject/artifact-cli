__all__ = ['HelpOperation', 'ListOperation', 'UploadOperation', 'DownloadOperation', 'InfoOperation']
from .help import HelpOperation
from .list import ListOperation
from .upload import UploadOperation
from .download import DownloadOperation
from .info import InfoOperation


def make(command, group_id, args, options):
    """
    Generate operation class from arguments.
    :param command: command string
    :param group_id: group id
    :param args: list of argument
    :param options: dict of options
    :return: Raise AssertionError when failure
    """
    if command == 'list':
        return ListOperation(group_id, args, options['output'])
    if command == 'upload':
        return UploadOperation(group_id, args, options['force'], options['print_only'])
    if command == 'download':
        return DownloadOperation(group_id, args, options['print_only'])
    if command == 'info':
        return InfoOperation(group_id, args, options['output'])
    raise AssertionError('Unknown command: %s' % command)
