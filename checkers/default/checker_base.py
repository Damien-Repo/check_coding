from checkers.ichecker import IChecker
from lib.icheck_exception import *


class CheckerBase(IChecker):

    @IChecker.check_by('file')
    def check_file_length(self, src_file):
        if len(src_file) > 20:
            raise CheckError('File length > 20')

    @IChecker.check_by('line')
    def check_length(self, src_line):
        if len(src_line.raw) > 60:
            raise CheckError('Length > 60')
