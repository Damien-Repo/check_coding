import sys
from tqdm import tqdm

from lib.config import Config
from lib.source_file import AllSourceLine

from outcomes.ioutcome import IOutcome


class OutcomeTqdm(IOutcome):

    def __init__(self):
        self._progress_steps = [tqdm(leave=False)]

    def __del__(self):
        self._cur_step.close()

    @property
    def _cur_step(self):
        assert(len(self._progress_steps) >= 1)
        return self._progress_steps[-1]

    def _align_desc(self):
        if len(self._progress_steps) == 0:
            return

        desc_max_len = len(max(self._progress_steps, key=lambda x: len(x.desc.rstrip())).desc.rstrip())
        for t in self._progress_steps:
            desc = t.desc.rstrip()
            if len(desc) <= desc_max_len:
                t.set_description_str(desc + ' ' * (desc_max_len - len(desc)))

    def print(self, msg, file=sys.stderr, *args, **kwargs):
        #//TEMP https://stackoverflow.com/questions/17772255/python-write-colored-text-in-file
        self._cur_step.write(str(msg), file=file)

    def error(self, msg):
        self.print(f'Error: {msg}', file=sys.stderr)

    def warning(self, msg):
        self.print(f'Warning: {msg}', file=sys.stderr)

    def info(self, msg):
        self.print(f'Info: {msg}', file=sys.stderr)

    @staticmethod
    def _format_exception_header(exc):
        colors = Config().Outcome.Tqdm.PrintColors
        return f'[{colors.level.get(exc.level_str, "")}{exc.level_str}{colors.none}]' \
               f'{colors.src_file_name}{exc.src_file_name}{colors.none}:' \
               f'{colors.line}{exc.pos.line_str}{colors.none}:' \
               f'{colors.checker_name}{exc.checker_name}->{colors.check_name}{exc.check_name}{colors.none}: ' \
               f'{colors.message}{str(exc)}{colors.none}'

    @staticmethod
    def _format_exception_body(exc):
        colors = Config().Outcome.Tqdm.PrintColors
        out = ''
        src_line = exc.src_line
        for line_pos in range(exc.pos.line_start, exc.pos.line_end + 1):
            out += f'\n  {colors.src_line}'
            if exc.error_pos.line_start <= line_pos <= exc.error_pos.line_end:
                col_start = 0
                col_end = -1
                if line_pos == exc.error_pos.line_start:
                    col_start = exc.error_pos.col_start - 1
                if line_pos == exc.error_pos.line_end:
                    col_end = exc.error_pos.col_end - 1
                out += f'{src_line.raw.clever_sub_str(end=col_start)}' \
                       f'{colors.src_line_error}' \
                       f'{src_line.raw.clever_sub_str(start=col_start, end=col_end)}' \
                       f'{colors.none}' \
                       f'{src_line.raw.clever_sub_str(start=col_end)}'
            else:
                out += f'{src_line.raw.clever}'
            out += f'{colors.none}'
            src_line = src_line.next()

        return out

    def _get_str_from_exception(self, check_exception):
        out = self._format_exception_header(check_exception)
        if isinstance(check_exception.src_line, AllSourceLine):
            out += self._format_exception_body(check_exception)

        return out

    def set_result(self, check_exception, *args, **kwargs):
        self.print(self._get_str_from_exception(check_exception), file=sys.stdout)

    def progress_start(self, title, total_size, unit):
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

    def progress_set_name(self, name, *args, **kwargs):
        self._cur_step.set_postfix_str(name)

    def progress_update(self, *args, **kwargs):
        self._cur_step.update(1)

    def progress_stop(self, *args, **kwargs):
        t = self._progress_steps.pop()
        t.close()
        self._align_desc()
