#!/usr/bin/env python

from lib.log import Log
from lib.config import Config
from lib.source_file import SourceFile
from checkers import CheckerManager


class App:

    def __init__(self, files_to_check, config=Config):
        assert len(files_to_check) > 0, 'No files given'
        self.config = config

        Log()

        self._src_files = []
        with Log().progress('Loading files', len(files_to_check), ' file') as log:
            for f in files_to_check:
                log.progress_set_name(f)
                self._src_files.append(SourceFile(f, config=self.config))
                log.progress_update()

        self._checkers = CheckerManager(config=self.config)

    def run(self):
        with Log().progress('Checking files', len(self._src_files), ' file') as log:
            for src_file in self._src_files:
                log.progress_set_name(src_file)
                self._checkers.process(src_file)
                log.set_result(src_file, self._checkers.get_result())
                log.progress_update()


if __name__ == '__main__':
    import sys
    conf_file = 'custom/conf/conf_example.py'
    a = App(sys.argv[1:], config=Config.load(conf_file))
    a.run()
