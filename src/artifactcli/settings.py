import logging
from driver import S3Driver
from os.path import expanduser, expandvars
import operation as op
from operation import HelpOperation
from repository import Repository
from util import CaseClass
import argparser


class Settings(CaseClass):
    """
    Manages all settings
    """
    parser = argparser.get_parser()

    def __init__(self, log_level=logging.INFO, operation=None, options=None, repo=None):
        super(Settings, self).__init__(['log_level', 'operation', 'options', 'repo'])

        # fallback operation
        operation = operation or HelpOperation(self.parser)

        # set parameters
        self.log_level = logging.DEBUG if options and options['debug'] else log_level
        self.operation = operation
        self.repo = repo
        self.options = options

    def configure_logging(self):
        """
        Setup logging settings
        """
        logging.basicConfig(level=self.log_level, format='[%(levelname)s] %(message)s')
        return self

    def parse_args(self, argv):
        """
        Parse command line arguments and update operation and options
        """
        options, args = Settings.parser.parse_args(argv[1:])
        if len(args) < 2:
            return self

        opt_dict = vars(options)
        try:
            operation = op.make(args[0], args[1], args[2:], opt_dict)
        except AssertionError:
            return self

        return Settings(self.log_level, operation, opt_dict, self.repo)

    def load_config(self):
        """
        Load configuration file and set repo
        """
        if self.options is None:
            return Settings(self.log_level)

        group_id = self.operation.group_id
        if not group_id:
            logging.error('Failed to load config: group id is not set in operation')
            return Settings(self.log_level)

        access_key = self.options['access_key']
        secret_key = self.options['secret_key']
        bucket = self.options['bucket']
        config = self.options['config']
        region = self.options['region']

        if not all([access_key, secret_key, bucket]):
            # command line arguments are prior to the configuration file
            path = expandvars(expanduser(config))

            try:
                with open(path) as fp:
                    a, s, b, r = self._read_aws_config(fp, group_id)
                    access_key = a if access_key is None else access_key
                    secret_key = s if secret_key is None else secret_key
                    bucket = b if bucket is None else bucket
                    region = r if region is None else region
            except IOError:
                logging.error('Failed to open configuration file: %s' % config)
                return Settings(self.log_level)

        for x, arg, opt in [
            (access_key, 'access_key', '--access'),
            (secret_key, 'secret_key', '--secret'),
            (bucket, 'bucket', '--bucket'),
        ]:
            if x is None:
                logging.error('Oops! "%s" setting is missing.' % arg)
                logging.error('Use "%s" option or write configuration file: %s' % (opt, config))
                return Settings(self.log_level)

        # set repository driver
        driver = S3Driver(access_key, secret_key, bucket, group_id, region)
        repo = Repository(driver, group_id)
        return Settings(self.log_level, self.operation, self.options, repo)

    @classmethod
    def _read_aws_config(cls, fp, group_id):
        import ConfigParser

        parser = ConfigParser.SafeConfigParser()
        parser.readfp(fp)

        # use group id as section name
        section_name = group_id if parser.has_section(group_id) else 'default'

        def f(attr):
            return parser.get(section_name, attr) if parser.has_option(section_name, attr) else None

        access_key = f('aws_access_key_id')
        secret_key = f('aws_secret_access_key')
        bucket = f('bucket')
        region = f('region')

        return access_key, secret_key, bucket, region
