
from lib.outcomes.ioutcome import IOutcome


class OutcomeUTest(IOutcome):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.steps = []
        self._data = []

    def print(self, msg):
        #print('print', msg)
        pass

    def error(self, msg):
        #print('error', msg)
        pass

    def warning(self, msg):
        #print('warning', msg)
        pass

    def info(self, msg):
        #print('info', msg)
        pass

    def set_result(self, check_exception, *args, **kwargs):
        #print('set_result', check_exception.pos.line_start)
        self._data.append(check_exception)

    def progress_start(self, title, total_size, unit):
        #print('>>>>>progress_start', title)
        if len(self.steps) == 0:
            self._data = []
        self.steps.append(title)

    def progress_set_name(self, name):
        #print('progress_set_name', name)
        pass

    def progress_update(self):
        #print('progress_update')
        pass

    def progress_stop(self):
        self.steps.pop()
        #print('<<<<<progress_stop', self.steps.pop())
        pass

    def get_outcome(self):
        return self._data
