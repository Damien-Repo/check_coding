from checkers.ichecker import IChecker
from lib.log import Log


class CheckerExample(IChecker):

    @IChecker.check_file
    def check_file_example(self, src_file):
        Log().print(f'Example check file {src_file}')
        pass

    @IChecker.check_line
    def check_line_example(self, src_line):
        #Log().print(f'Example check line {src_line}')
        pass
