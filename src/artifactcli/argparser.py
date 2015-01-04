from optparse import OptionParser

VERSION = 'artifact-cli 0.0.5'
USAGE = """
  %prog [options] list     GROUP
  %prog [options] upload   GROUP LOCAL_PATH
  %prog [options] download GROUP LOCAL_PATH [REVISION | latest]
  %prog [options] info     GROUP FILE_NAME  [REVISION | latest]
  %prog [options] delete   GROUP FILE_NAME   REVISION

  e.g.
   GROUP     : your.company
   LOCAL_PATH: /path/to/awesome/target/scala-2.11/awesome-assembly-1.2.3.jar
   FILE_NAME : awesome-assembly-1.2.3.jar
   REVISION  : 10"""

DEFAULT_CONF_PATH = '~/.artifact-cli'


def get_parser():
    """
    Get command line arguments parser
    """
    parser = OptionParser(usage=USAGE, version=VERSION)

    parser.add_option(
        '--config', dest='config', default=DEFAULT_CONF_PATH, type='string',
        help='path to the config file'
    )
    parser.add_option(
        '--check', action='store_true', dest='print_only', default=False,
        help='prints only the information to upload, download or delete'
    )
    parser.add_option(
        '--force', action='store_true', dest='force', default=False,
        help='upload file even when it is already registered to the repository'
    )
    parser.add_option(
        '--output', dest='output', default=None,
        help='specify output format, "text" or "json" (default: text)'
    )
    parser.add_option(
        '--access', dest='access_key', default=None, type='string',
        help='AWS access key id'
    )
    parser.add_option(
        '--secret', dest='secret_key', default=None, type='string',
        help='AWS secret access key'
    )
    parser.add_option(
        '--bucket', dest='bucket', default=None, type='string',
        help='Amazon S3 bucket name'
    )
    parser.add_option(
        '--region', dest='region', default=None, type='string',
        help='Amazon S3 region name (default: us-east-1)'
    )
    return parser
