import os

from lib.log import Log
from lib.utils import PluginManager
from lib.config import Config

from checkers.ichecker import IChecker
from lib.source_file import SourceFile


class CheckerManager(PluginManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._load_plugins(IChecker, os.path.join('checkers', 'default'), 'checker_')
        self._load_plugins(IChecker, os.path.join(Config().CUSTOM_ROOT_PATH, 'checkers'), 'checker_')

    def process(self, src_file):
        with Log().progress('Check', len(self), ' checker') as log:
            for checker_name, checker in self:
                log.progress_set_name(checker_name)
                checker.process(src_file)
                log.progress_update()

    def get_result(self):
        out_res = {}
        for checker_name, checker in self:
            for check_exception in checker.get_result():
                src_line = check_exception.src_line
                check_name = check_exception.check_name
                if isinstance(src_line, SourceFile):
                    row = 0
                else:
                    row = src_line.row

                if row not in out_res:
                    out_res[row] = {}
                if checker_name not in out_res[row]:
                    out_res[row][checker_name] = {}
                if check_name not in out_res[row][checker_name]:
                    out_res[row][checker_name][check_name] = []
                out_res[row][checker_name][check_name].append(check_exception)

        return out_res
