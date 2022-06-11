#!/usr/bin/env python

from source_file import SourceFile
from checkers import Checkers
from log import OutputLog


class App:

    def __init__(self, files_to_check):
        assert len(files_to_check) > 0, 'No files given'

        OutputLog()

        self._src_files = []
        with OutputLog().progress('Loading files', len(files_to_check), ' file') as log:
            for f in files_to_check:
                log.progress_set_name(f)
                self._src_files.append(SourceFile(f))
                log.progress_update()

        self._checkers = Checkers()

    def run(self):
        with OutputLog().progress('Checking files', len(self._src_files), ' file') as log:
            for src_file in self._src_files:
                log.progress_set_name(src_file)
                self._checkers.process(src_file)
                log.set_result(src_file, self._checkers.get_result())
                log.progress_update()
        '''
        res = self._checkers.get_result()
        for f, c in res.items():
            for line_index in sorted(c.keys()):
                print(f'{f}:{line_index}:')
                for checker_name, checker in c[line_index].items():
                    for check_name, check in checker.items():
                        print(f'   {checker_name}.{check_name}: {check["message"]}')
                    print(f'{check["line"].raw}')
        '''


if __name__ == '__main__':
    import sys
    #a = App(sys.argv[1:])
    #a.run()
    from loaders import *

    def dump(l):
        for i, lines in l:
            for line in lines:
                print('%4d' % (i), line)

    #dump(LoaderPP('test_file.c'))
    #print('===========================')
    #dump(LoaderPPKeepComment('test_file.c'))
    #print('===========================')
    dump(LoaderASTClang('test_file.c'))
    #print('===========================')
    #dump(LoaderRaw('test_file.c'))
