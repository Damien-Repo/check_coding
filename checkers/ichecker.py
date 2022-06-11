#!/usr/bin/env python

from log import OutputLog


class CheckError(Exception):
    pass

from time import sleep


class IChecker:

    checks = {}

    def __init__(self, source_file):
        self._source_file = source_file
        self._result = []

    @property
    def src(self):
        return self._source_file

    @staticmethod
    def _check_decorator(function, mode):
        def wrapper(self, src):
            try:
                function(self, src)
            except CheckError as e:
                self._result.append((function.__name__, src, e))

        if mode not in IChecker.checks:
            IChecker.checks[mode] = {}
        IChecker.checks[mode][function.__name__] = wrapper
        return wrapper

    @staticmethod
    def check_line(function):
        """Decorator to register a check line function"""
        return IChecker._check_decorator(function, 'line')

    @staticmethod
    def check_file(function):
        """Decorator to register a check file function"""
        return IChecker._check_decorator(function, 'file')

    def _check_by_file(self):
        with OutputLog().progress('Checking file', len(IChecker.checks['file']), 'checks') as log:
            for identifier, check in IChecker.checks['file'].items():
                log.progress_set_name(f'{identifier}')
                check(self, self.src)
                log.progress_update()

    def _check_by_line(self):
        with OutputLog().progress('Checking lines', len(self.src) + len(IChecker.checks['line']), 'checks') as log:
            for i, src_line in enumerate(self.src):
                for identifier, check in IChecker.checks['line'].items():
                    log.progress_set_name(f'{i}:{identifier}')
                    check(self, src_line)
                    log.progress_update()

    def process(self):
        for mode in IChecker.checks:
            getattr(self, f'_check_by_{mode}', lambda: None)()

    def get_result(self):
        return self._result
