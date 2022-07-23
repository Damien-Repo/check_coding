from lib.config import Config
from lib.log import Log
from lib.source_file import AllSourceLine
from lib.icheck_exception import *

from checkers.ichecker import IChecker


class CheckerExample(IChecker):

    @IChecker.check_by('file')
    def check_blacklist(self, _):
        raise CheckError(f'You should never call this check !!')

    @IChecker.check_by('file')
    def check_file_example(self, src_file):
        Log().print(f'Example check file {src_file}')
        len_max = Config().Checker.CheckerExample.get('FILE_LENGTH_MAX', 1)
        check_exceptions = [CheckInfo, CheckWarning, CheckError]
        with CheckExceptionList().context() as EL:
            for i, Check in enumerate(check_exceptions, start=1):
                with EL.check():
                    if len(src_file) > len_max * i:
                        raise Check(f'File length > {len_max * i}')

    @IChecker.check_by('line')
    def check_line_example(self, src_line: AllSourceLine):
        levels = {'INFO': CheckInfo, 'WARNING': CheckWarning, 'ERROR': CheckError}
        for lvl, Check in levels.items():
            lines_error = Config().Checker.CheckerExample.get(f'LINES_{lvl}', [])
            if src_line.row in lines_error:
                raise Check(f'Line {src_line.row}')

    @IChecker.check_by('function')
    def check_function_example(self, src_line: AllSourceLine):
        params = [x for x in src_line.ast[0].cursor.get_children() if x.kind.name == 'PARM_DECL']
        param_count_max = Config().Checker.CheckerExample.get('PARAM_COUNT_MAX', 0)
        if len(params) > param_count_max:
            start = params[param_count_max].extent.start
            end = params[-1].extent.end
            pos = {'line_end': end.line, 'col_end': end.column}
            pos_err = {
                'line_start': start.line, 'col_start': start.column,
                'line_end': end.line, 'col_end': end.column,
            }
            raise CheckWarning('Too many parameters', error_pos=pos_err, context_pos=pos)

