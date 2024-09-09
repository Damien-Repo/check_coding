import sys
from tqdm import tqdm

from lib.config import Config
from lib.source_file import AllSourceLine

from lib.outcomes.ioutcome import IOutcome

__default_config__ = {
    'Outcome': {
        'Tqdm': {
            'PrintColors': {
                'check_name': '',
                'checker_name': '',
                'level': {
                    'ERRO': '',
                    'WARN': '',
                    'INFO': ''
                },
                'line': '',
                'id_str': '',
                'message': '',
                'no_color': '',
                'src_file_name': '',
                'src_line': '',
                'src_line_error': ''
            }
        }
    }
}


class OutcomeTqdm(IOutcome):

    def __init__(self):
        self._progress_steps = []

    def __del__(self):
        print()  # print new line for prompt

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

    def print(self, msg, file = sys.stderr):
        #//TEMP https://stackoverflow.com/questions/17772255/python-write-colored-text-in-file
        try:
            self._cur_step.write(f'{msg}', file=file)
        except AssertionError:
            print(f'{msg}', file=file)

    def error(self, msg):
        self.print(f'Error: {msg}')

    def warning(self, msg):
        self.print(f'Warning: {msg}')

    def info(self, msg):
        self.print(f'Info: {msg}')

    def debug(self, msg):
        self.print(f'Debug: {msg}')

    @staticmethod
    def _format_exception_header(exc):
        colors = Config().Outcome.Tqdm.PrintColors
        return f'[{colors.level.get(exc.level_str, "")}{exc.level_str}{colors.no_color}]' \
               f'{colors.src_file_name}{exc.src_file_name}{colors.no_color}:' \
               f'{colors.line}{exc.pos.line_str}{colors.no_color}:' \
               f'{colors.checker_name}{exc.checker_name}->{colors.check_name}{exc.check_name}{colors.no_color}: ' \
               f'{colors.message}{str(exc)}{colors.no_color}'

    @staticmethod
    def _format_exception_body(exc):
        colors = Config().Outcome.Tqdm.PrintColors
        out = ''
        if exc.message_details is not None:
            out += f'\n{colors.message_details}{exc.message_details}{colors.no_color}'

        if not isinstance(exc.src_line, AllSourceLine):
            return out

        src_line = exc.src_line
        for line_pos in range(exc.pos.line_start, exc.pos.line_end + 1):

            out += f'\n{src_line.line_number: 4}|  {colors.src_line}'

            if exc.error_pos.line_start <= line_pos <= exc.error_pos.line_end:
                col_start = 0
                col_end = -1
                if line_pos == exc.error_pos.line_start:
                    col_start = exc.error_pos.col_start - 1
                if line_pos == exc.error_pos.line_end:
                    col_end = exc.error_pos.col_end - 1

                out += f'{"".join([l.clever_sub_str(end=col_start) for l in src_line.raw])}' \
                       f'{colors.src_line_error}' \
                       f'{"".join([l.clever_sub_str(start=col_start, end=col_end) for l in src_line.raw])}' \
                       f'{colors.no_color}' \
                       f'{"".join([l.clever_sub_str(start=col_end) for l in src_line.raw])}'
            else:
                out += f'{"".join([l.clever for l in src_line.raw])}'

            out += f'{colors.no_color}'
            src_line = src_line.next()

        return out

    def _get_str_from_exception(self, check_exception):
        out = self._format_exception_header(check_exception)
        out += self._format_exception_body(check_exception)
        return out

    def set_result(self, check_exception, *args, **kwargs):
        self.print(self._get_str_from_exception(check_exception), file=sys.stdout)

    @staticmethod
    def update_progress_bar_color(t: tqdm):
        '''
        Update progress bar color with gradient (red to green)
        '''
        res = int((t.n / t.total) * 255 * 2)
        r = 255
        g = 255
        if res > 255:
            r = 255 - (res - 255)
        else:
            g = res
        t.colour = f'#{r:02x}{g:02x}00'

    def progress_start(self, title, total_size, unit):
        desc = '  ' * len(self._progress_steps) + title

        t = tqdm(total=total_size,
                 ncols=None,
                 mininterval=.1,
                 leave=False,
                 position=len(self._progress_steps) + 1,
                 bar_format='{desc}: {percentage:3.0f}% {bar:100} {n_fmt:>3s} / {total_fmt:>3s}{postfix}{bar:-100b}',
                 #bar_format='{desc}: {bar}',  # variante plus sobre
                 ascii=' ┈─',
                 colour='#ff0000',
                 desc=desc,
                 unit=unit)

        self._progress_steps.append(t)
        self._align_desc()

    def progress_set_name(self, name):
        self._cur_step.set_postfix_str(name)

    def progress_update(self):
        self._cur_step.update(1)
        self.update_progress_bar_color(self._cur_step)

    def progress_stop(self):
        t = self._progress_steps.pop()
        t.close()
        self._align_desc()
