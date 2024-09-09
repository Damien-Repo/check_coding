import re

from lib.checkers.ichecker import IChecker
from lib.icheck_exception import *
from lib.filetypes import FileTypeDotH


class CheckerBase(IChecker):

    @IChecker.check_by('file')
    def check_file_length(self, src_file):
        if len(src_file) > 20:
            raise CheckError('File length > 20')

    @IChecker.check_by('line')
    def check_line_length(self, src_line):
        if len(src_line.raw) > 60:
            raise CheckError('Line length > 60')

    @IChecker.check_by('file', filetypes=[FileTypeDotH])
    def check_header_protection(self, src_file):
        #//TEMP le format du expected_define doit etre configurable
        normalized_name = '_'.join(re.split(r'[-_. ]+', src_file.file_name)).upper()
        expected_define = f'__{normalized_name}__'
        #//TEMP le pattern doit etre configurable aussi, format string autorise
        pattern = f'''.*
#ifndef {expected_define}
#define {expected_define}

.*

#endif\t/\\* {expected_define} \\*/
'''
        self.check_pattern(pattern, src_file.get_content('raw'), 'Header protection not found')

