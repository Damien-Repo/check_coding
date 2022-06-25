from tqdm import tqdm
from contextlib import contextmanager

from lib.utils import Singleton
from lib.source_file import AllSourceLine


class Log(metaclass=Singleton):

    def __init__(self, quiet=False):
        self._quiet = quiet
        self._progress_steps = []

    @property
    def cur_step(self):
        return self._progress_steps[-1]

    def _align_desc(self):
        if len(self._progress_steps) == 0:
            return

        desc_max_len = len(max(self._progress_steps, key=lambda x: len(x.desc.rstrip())).desc.rstrip())
        for t in self._progress_steps:
            desc = t.desc.rstrip()
            if len(desc) <= desc_max_len:
                t.set_description_str(desc + ' ' * (desc_max_len - len(desc)))

    def print(self, msg):
        #//TEMP https://stackoverflow.com/questions/17772255/python-write-colored-text-in-file
        self.cur_step.write(msg)

    def progress_start(self, title='', total_size=None, unit=''):
        desc = '  ' * len(self._progress_steps) + title

        t = tqdm(total=total_size,
                 ncols=None,
                 mininterval=.1,
                 leave=False,
                 colour='green',
                 position=len(self._progress_steps) + 1,
                 desc=desc,
                 unit=unit)

        self._progress_steps.append(t)
        self._align_desc()

    def progress_set_name(self, name):
        self.cur_step.set_postfix_str(name)

    def progress_update(self):
        self.cur_step.update(1)

    def progress_stop(self):
        t = self._progress_steps.pop()
        t.close()
        self._align_desc()

    @contextmanager
    def progress(self, *args, **kwargs):
        try:
            self.progress_start(*args, **kwargs)
            yield self
        finally:
            self.progress_stop()

    def set_result(self, src_file, result):
        #//TEMP creer un obj result
        for line, res in sorted(result.items()):
            for checker, check in sorted(res.items()):
                for check_name, check_res in sorted(check.items()):
                    self.print(f'\x1B[34;1m{src_file}\x1B[0m:'
                               f'\x1B[33;1m{line}\x1B[0m:'
                               f'\x1B[36;1m{checker}->{check_name}\x1B[0m: '
                               f'\x1B[31;1m{check_res["message"]}\x1B[0m')
                    if isinstance(check_res['line'], AllSourceLine):
                        self.print(f'  {check_res["line"].raw}')
