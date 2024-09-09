import re
from typing import Generator

from lib.log import Log
from lib.icheck_exception import ICheckException, CheckExceptionList, CheckError
from lib.config import Config
from lib.loaders import LoaderManager


class IChecker:

    _checks = {}

    def __init__(self):
        self._source_file = None
        self._result = []
        self.has_succeeded = True

    @property
    def src(self):
        return self._source_file

    @staticmethod
    def _check_decorator(function, mode, filetypes=None):
        def wrapper(self, src):
            try:
                function(self, src)
            except ICheckException as e:
                e.checker_name = self.__class__.__name__
                e.src_line = src
                self._result.append(e)
                self.has_succeeded = False
            except CheckExceptionList as el:
                self.has_succeeded = False
                for e in el:
                    e.checker_name = self.__class__.__name__
                    e.src_line = src
                    self._result.append(e)

        module = function.__globals__['__name__']
        if module not in IChecker._checks:
            IChecker._checks[module] = {}
        if mode not in IChecker._checks[module]:
            IChecker._checks[module][mode] = {}
        name = module[module.index('checkers.') + len('checkers.'):module.rindex('.')]
        name += f'.{function.__qualname__}'
        IChecker._checks[module][mode][name] = {
            'func': wrapper,
            'filetypes': filetypes,
        }
        return wrapper

    @property
    def checks(self):
        def is_allowed(name):
            allowed = True
            if Config().Checker.WHITELIST is not None:
                checkers = [x for x in Config().Checker.WHITELIST
                            if (x[-2:] == '.*' and name.startswith(x[:-2])) or name == x]
                if len(checkers) == 0:
                    #print('> WL!!', name, checkers, Config().Checker.WHITELIST)
                    allowed = False

            if Config().Checker.BLACKLIST is not None:
                checkers = [x for x in Config().Checker.BLACKLIST
                            if (x[-2:] == '.*' and name.startswith(x[:-2])) or name == x]
                if len(checkers) > 0:
                    #print('> BL!!', name, checkers)
                    allowed = False

            #print('>', name, 'allowed:', allowed)
            return allowed

        out = {
            mode: {
                name: func
                for name, func in funcs.items()
                if is_allowed(name)
            }
            for mode, funcs in IChecker._checks[self.__class__.__module__].items()
        }
        return out

    @staticmethod
    def check_by(mode: str, filetypes: (list, tuple) = None):
        """Decorator to register a check function"""
        def wrapper(function):
            return IChecker._check_decorator(function, mode, filetypes)
        return wrapper

    def _run_check_by(self, mode, checks, mode_gen):
        count = len(list(mode_gen(self.src))) + len(checks)
        # print(f'>>>> AAA {mode_gen}: {list(mode_gen(self.src))}')
        with Log().progress(f'Checking {mode}s', count, 'checks') as log:
            # print(f'>>>> BBB')
            for i, src_line in enumerate(mode_gen(self.src)):
                # print(f'>>>> CCC')
                for identifier, check in checks.items():
                    # print(f'>> {identifier}: {check}')
                    if check['filetypes'] is not None and self.src.type not in check['filetypes']:
                        Log().debug(f'Skip check {identifier} for type {self.src.type.__class__.__name__}')
                        continue
                    log.progress_set_name(f'{i}:{identifier.rsplit(".")[-1]}')
                    check['func'](self, src_line)
                    log.progress_update()

    def process(self, source_file):
        self._source_file = source_file
        self._result = []
        self.has_succeeded = True

        check_by = LoaderManager().get_check_by()
        # print(f'>>>>>XX {self.checks} => {source_file}')
        for mode, checks in self.checks.items():
            # print(f'>>>>> {mode}: {checks}')
            if mode not in check_by:
                Log().warning(f'You need to use the appropriate loader to use check_by("{mode}") => all checks ignored !')
                # print(f'>> continue')
                continue
            # try:
                # print(f'>> run')
            self._run_check_by(mode, checks, check_by[mode])
            # except AttributeError as e:
            #     Log().error(f'{e}')

    def get_result(self):
        assert(not self.has_succeeded and len(self._result) > 0)
        return self._result

    @staticmethod
    def check_pattern(pattern: str, content: str, exception_id_str: str,
                      exception: ICheckException = CheckError, message_details: str = None):
        if isinstance(content, Generator):
            content = '\n'.join(content)

        match = re.fullmatch(pattern, content, re.MULTILINE | re.DOTALL)
        if match:
            return match

        sub_patterns = re.split('\n', pattern)
        for i in range(1, len(sub_patterns)):
            sub_pattern = '\n'.join(sub_patterns[0:i])
            if not re.findall(sub_pattern, content, re.MULTILINE | re.DOTALL):
                expected = '\n'.join(sub_patterns[i - 1:i])
                if message_details is None:
                    message_details = "Expected '{expected}' line not found"
                raise exception(exception_id_str, message_details=message_details.format(expected=expected))
