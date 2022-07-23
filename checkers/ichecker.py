from lib.log import Log
from lib.icheck_exception import ICheckException, CheckExceptionList
from lib.config import Config


class IChecker:

    _checks = {}

    def __init__(self):
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
            except ICheckException as e:
                e.checker_name = self.__class__.__name__
                e.src_line = src
                self._result.append(e)
            except CheckExceptionList as el:
                for e in el:
                    e.checker_name = self.__class__.__name__
                    e.src_line = src
                    self._result.append(e)

        module = function.__globals__['__name__']
        if module not in IChecker._checks:
            IChecker._checks[module] = {}
        if mode not in IChecker._checks[module]:
            IChecker._checks[module][mode] = {}
        IChecker._checks[module][mode][function.__name__] = wrapper
        return wrapper

    @property
    def checks(self):
        out = {
            mode: {
                name: func
                for name, func in funcs.items()
                if Config().Checker.BLACKLIST is None or
                    f'{self.__class__.__name__}.{name}' not in Config().Checker.BLACKLIST
            }
            for mode, funcs in IChecker._checks[self.__class__.__module__].items()
        }
        return out

    @staticmethod
    def check_by(mode: str):
        """Decorator to register a check function"""
        def wrapper(function):
            return IChecker._check_decorator(function, mode)
        return wrapper

    def _run_check_by(self, mode, checks, mode_gen):
        count = len(list(mode_gen(self.src))) + len(checks)
        with Log().progress(f'Checking {mode}s', count, 'checks') as log:
            for i, src_line in enumerate(mode_gen(self.src)):
                for identifier, check in checks.items():
                    log.progress_set_name(f'{i}:{identifier}')
                    check(self, src_line)
                    log.progress_update()

    def process(self, source_file):
        self._source_file = source_file
        self._result = []

        check_by = self.src.loaders.get_check_by()
        for mode, checks in self.checks.items():
            if mode not in check_by:
                Log().print(f'You need to use the appropriate loader to use check_by("{mode}") => all checks ignored !')
                continue
            try:
                self._run_check_by(mode, checks, check_by[mode])
            except AttributeError as e:
                Log().error(f'{e}')

    def get_result(self):
        return self._result
