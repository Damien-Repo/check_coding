#!/usr/bin/env python

from lib.log import Log
from lib.config import Config
from lib.source_file import SourceFile
from checkers import CheckerManager


class App:

    def __init__(self, config_file, files_to_check=[], dump_conf=None):
        Config(config_file)
        if dump_conf is not None:
            Log().print('=== Config begin ===')
            Log().print(f'{Config().dump(dump_conf)}')
            Log().print('=== Config end ===')

        # remove duplicates file name
        files_to_check = {f.name: f for f in files_to_check}.values()

        self._src_files = []
        with Log().progress('Loading files', len(files_to_check), ' file') as log:
            for f in files_to_check:
                log.progress_set_name(f.name)
                self._src_files.append(SourceFile(f))
                log.progress_update()

        self._checkers = CheckerManager()

    def run(self):
        with Log().progress('Checking files', len(self._src_files), ' file') as log:
            for src_file in self._src_files:
                log.progress_set_name(src_file)
                self._checkers.process(src_file)
                log.set_result(self._checkers.get_result())
                log.progress_update()


if __name__ == '__main__':
    import sys
    import argparse
    parser = argparse.ArgumentParser(prog=sys.argv[0])
    parser.add_argument('-c', '--conf',
                        type=argparse.FileType('r'),
                        dest='config_file',
                        metavar='config_file',
                        help='the configuration file to use')
    parser.add_argument('-d', '--dump-conf',
                        choices=['str', 'json'],
                        type=str,
                        nargs='?',
                        const='str',
                        default=None,
                        dest='dump_conf',
                        help='dump the using configuration file')
    parser.add_argument('files_to_check',
                        type=argparse.FileType('r'),
                        nargs='*',
                        metavar='file_to_check',
                        help='the file to check')
    args = parser.parse_args()
    a = App(**vars(args))
    a.run()
