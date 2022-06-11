#!/usr/bin/env python

from checkers.ichecker import IChecker, CheckError

from log import OutputLog


class CheckerBase(IChecker):

    @IChecker.check_line
    def check_length(self, src_line):
        if len(src_line.raw) > 10:
            raise CheckError('Length > 10')
