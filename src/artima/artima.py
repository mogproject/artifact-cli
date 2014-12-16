#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import expanduser
import sys
from repository import Repository
from driver import S3Driver
from artifact import Artifact

DEFAULT_CONF_PATH = expanduser('~/.artima')


def parse_args():
    """
    Parse command line arguments
    """
    from optparse import OptionParser

    usage = """
    %prog list     GROUP [options]
    %prog upload   GROUP LOCAL_PATH [options]
    %prog download GROUP LOCAL_PATH [REVISION | latest] [options]

        e.g.
        GROUP     : your.company
        LOCAL_PATH: /proj/awesome/target/scala-2.11/awesome-assembly-1.2.3-SNAPSHOT.jar
        REVISION  : 10

        options:
          --config CONFIG   path to the config file
          --check
    """
    parser = OptionParser(usage=usage)

    parser.add_option(
        '--config', dest='config', default=DEFAULT_CONF_PATH, type='string',
        help='path to the config file'
    )
    parser.add_option(
        '--check', action='store_true', dest='check', default=False,
        help='prints only the information to upload or download'
    )

    options, args = parser.parse_args()

    try:
        options.command = args[0]
        options.group_id = args[1]
        if options.command == 'list':
            pass
        elif options.command == 'upload':
            options.local_path = args[2]
        elif options.command == 'download':
            options.local_path = args[2]
            options.revision = args[3]
        else:
            raise RuntimeError('invalid command: %s' % options.command)
    except IndexError:
        parser.print_usage()
        sys.exit(1)

    return options


def load_config(config_fp, group_id):
    """
    Load configuration file
    """
    import ConfigParser

    parser = ConfigParser.SafeConfigParser()
    parser.readfp(config_fp)

    section_name = group_id if parser.has_section(group_id) else 'default'

    access_key = parser.get(section_name, 'aws_access_key_id')
    secret_key = parser.get(section_name, 'aws_secret_access_key')
    bucket_name = parser.get(section_name, 'bucket_name')

    return access_key, secret_key, bucket_name


def main():
    """
    Main function
    """

    # get command line arguments
    options = parse_args()

    # load config
    try:
        with open(options.config) as fp:
            access_key, secret_key, bucket_name = load_config(fp, options.group_id)
    except:
        print('Failed to load config: %s' % options.config)
        return 1

    driver = S3Driver(access_key, secret_key, bucket_name)
    repo = Repository(driver)

    if options.command == 'list':
        repo.load()
        repo.print_list()
    elif options.command == 'upload':
        repo.load()
        repo.upload(options.group_id, options.local_path)
    elif options.command == 'download':
        repo.download(options.group_id, options.local_path)
    return 0


if __name__ == '__main__':
    sys.exit(main())
