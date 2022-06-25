from lib.log import Log
from lib.config import Config


class CheckError(Exception):
    pass


class IChecker:

    _checks = {}

    def __init__(self, config=Config):
        self.config = config
        self._source_file = None
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

        module = function.__globals__['__name__']
        if module not in IChecker._checks:
            IChecker._checks[module] = {}
        if mode not in IChecker._checks[module]:
            IChecker._checks[module][mode] = {}
        IChecker._checks[module][mode][function.__name__] = wrapper
        return wrapper

    @property
    def checks(self):
        return IChecker._checks[self.__class__.__module__]

    @staticmethod
    def check_line(function):
        """Decorator to register a check line function"""
        return IChecker._check_decorator(function, 'line')

    @staticmethod
    def check_file(function):
        """Decorator to register a check file function"""
        return IChecker._check_decorator(function, 'file')

    def _check_by_file(self):
        with Log().progress('Checking file', len(self.checks['file']), 'checks') as log:
            for identifier, check in self.checks['file'].items():
                log.progress_set_name(f'{identifier}')
                check(self, self.src)
                log.progress_update()

    def _check_by_line(self):
        with Log().progress('Checking lines', len(self.src) + len(self.checks['line']), 'checks') as log:
            for i, src_line in enumerate(self.src):
                for identifier, check in self.checks['line'].items():
                    log.progress_set_name(f'{i}:{identifier}')
                    check(self, src_line)
                    log.progress_update()

    def process(self, source_file):
        self._source_file = source_file
        self._result = []

        for mode in self.checks:
            getattr(self, f'_check_by_{mode}', lambda: None)()

    def get_result(self):
        return self._result
