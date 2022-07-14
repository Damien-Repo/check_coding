from checkers.ichecker import IChecker
from lib.log import Log
from lib.source_file import AllSourceLine
from lib.icheck_exception import *


class CheckerExample(IChecker):

    @IChecker.check_by('file')
    def check_file_example(self, src_file):
        Log().print(f'Example check file {src_file}')
        with CheckExceptionList().context() as EL:
            with EL.check():
                if len(src_file) > 5:
                    raise CheckInfo('File length > 5')

            with EL.check():
                if len(src_file) > 10:
                    raise CheckWarning('File length > 10')

            with EL.check():
                if len(src_file) > 15:
                    raise CheckError('File length > 15')

    @IChecker.check_by('line')
    def check_line_example(self, src_line: AllSourceLine):
        if src_line.row == 1:
            raise CheckInfo('Line 1')
        elif src_line.row == 2:
            raise CheckWarning('Line 2')
        elif src_line.row == 3:
            raise CheckError('Line 3')

    @IChecker.check_by('function')
    def check_function_example(self, src_line: AllSourceLine):
        params = [x for x in src_line.ast[0].cursor.get_children() if x.kind.name == 'PARM_DECL']
        param_count_max = 4
        if len(params) > param_count_max:
            start = params[param_count_max].extent.start
            end = params[-1].extent.end
            pos = {'line_end': end.line, 'col_end': end.column}
            pos_err = {
                'line_start': start.line, 'col_start': start.column,
                'line_end': end.line, 'col_end': end.column,
            }
            raise CheckWarning('Too many parameters', error_pos=pos_err, context_pos=pos)

