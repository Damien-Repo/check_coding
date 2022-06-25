import os

from lib.log import Log
from lib.utils import PluginManager

from checkers.ichecker import IChecker
from lib.source_file import SourceFile


class CheckerManager(PluginManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._load_plugins(IChecker, os.path.join('checkers', 'default'), 'checker_')
        self._load_plugins(IChecker, os.path.join(self.config.CUSTOM_ROOT_PATH, 'checkers'), 'checker_')

    def process(self, src_file):
        with Log().progress('Check', len(self), ' checker') as log:
            for checker_name, checker in self:
                log.progress_set_name(checker_name)
                checker.process(src_file)
                log.progress_update()

    def get_result(self):
        out_res = {}
        for checker_name, checker in self:
            for check_name, src_line, msg in checker.get_result():
                if isinstance(src_line, SourceFile):
                    row = 0
                else:
                    row = src_line.row

                if row not in out_res:
                    out_res[row] = {}
                if checker_name not in out_res[row]:
                    out_res[row][checker_name] = {}
                assert(check_name not in out_res[row][checker_name])
                out_res[row][checker_name][check_name] = {
                    'message': msg,
                    'line': src_line,
                }

        return out_res
