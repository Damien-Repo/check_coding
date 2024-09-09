import inspect

from contextlib import contextmanager

from lib.utils import Singleton

from lib.outcomes import OutcomeManager
from lib.outcomes import IOutcome


class Log(metaclass=Singleton):

    def __init__(self):
        self._outcomes = OutcomeManager()

        self._outcomes_func_name = [name
                                    for name, _ in inspect.getmembers(IOutcome, predicate=inspect.isfunction)
                                    if not name.startswith('_')]

    def __getattr__(self, item):
        if item not in self._outcomes_func_name:
            return getattr(self, item)

        def functor(*args, **kwargs):
            for _, outcome in self._outcomes:
                getattr(outcome, item)(*args, **kwargs)

        return functor

    def get_outcome(self, name):
        return self._outcomes[name].get_outcome()

    @contextmanager
    def progress(self, *args, **kwargs):
        try:
            self.progress_start(*args, **kwargs)
            yield self
        finally:
            self.progress_stop()

    def set_result(self, result, *args, **kwargs):
        for line, res in sorted(result.items()):
            for checker, check in sorted(res.items()):
                for check_name, exceptions in sorted(check.items()):
                    for e in exceptions:
                        for _, outcome in self._outcomes:
                            outcome.set_result(e, *args, **kwargs)
