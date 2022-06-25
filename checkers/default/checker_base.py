from checkers.ichecker import IChecker, CheckError


class CheckerBase(IChecker):

    @IChecker.check_file
    def check_file_length(self, src_file):
        if len(src_file) > 20:
            raise CheckError('File length > 20')

    @IChecker.check_line
    def check_length(self, src_line):
        if len(src_line.raw) > 20:
            raise CheckError('Length > 20')
