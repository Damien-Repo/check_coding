#!/usr/bin/env python

import sys
import argparse

from lib.check_coding import CheckCoding
from lib.utests import UTestManager
from lib.tools import SourceFileViewer


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=sys.argv[0])
    parser.add_argument('-c', '--conf',
                        type=argparse.FileType('r'),
                        dest='config_file',
                        metavar='config_file',
                        help='the configuration file to use')
    parser.add_argument('-d', '--dump-conf',
                        choices=['str', 'json', 'python'],
                        type=str,
                        nargs='?',
                        const='str',
                        default=None,
                        dest='dump_conf',
                        help='dump the using configuration file')
    parser.add_argument('-u', '--utests',
                        action='store_true',
                        dest='utests',
                        help='launch unit tests of selected loaders or checkers in config file')
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        dest='verbose',
                        help='verbose mode')
    parser.add_argument('-s', '--source-file-viewer',
                        action='store_true',
                        dest='source_file_viewer',
                        help='Source File Viewer tool')
    parser.add_argument('files_to_check',
                        type=argparse.FileType('r'),
                        nargs='*',
                        metavar='file_to_check',
                        help='the file to check')
    args = parser.parse_args()

    if args.utests:
        app = UTestManager(**vars(args))
    elif args.source_file_viewer:
        app = SourceFileViewer(**vars(args))
        app.run()
    else:
        app = CheckCoding(**vars(args))

    exit_code = 0 if app.has_succeeded else 1
    sys.exit(exit_code)
