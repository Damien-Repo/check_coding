from contextlib import contextmanager

from lib.source_file import AllSourceLine, SourceFile, SourceFilePos


class ICheckException(Exception):
    LEVEL = '00_NONE'

    def __init__(self, message, message_details=None, error_pos=None, context_pos=None, src_line=None):
        super().__init__(message)

        def create_pos(pos):
            if isinstance(pos, dict):
                return SourceFilePos(**pos)
            elif isinstance(pos, (tuple, list)):
                return SourceFilePos(*pos)
            elif isinstance(pos, SourceFilePos):
                return pos
            return SourceFilePos()

        self._message_details = message_details
        self._error_pos = create_pos(error_pos)
        self._context_pos = create_pos(context_pos)
        self.src_line = src_line
        self.checker_name = ''

    def __cmp__(self, other):
        return self.level.cmp(other.level)

    def __eq__(self, other):
        return (
                self.args == other.args and
                self.error_pos == other.error_pos and
                self.checker_name == other.checker_name and
                self.check_name == other.check_name
        )

    def __repr__(self):
        return f"{self.__class__.__name__}{self.error_pos}('{self.args[0]}')"

    @property
    def message_details(self):
        return self._message_details

    @property
    def error_pos(self):
        return self._error_pos

    @property
    def pos(self):
        return self._context_pos

    @property
    def src_line(self):
        return self._src_line

    @src_line.setter
    def src_line(self, value):
        if isinstance(value, AllSourceLine) and self.pos.line_start == 0:
            self.pos.line_start = value.line_number
        self._src_line = value

    @property
    def level(self):
        return int(self.LEVEL.split('_')[0])

    @property
    def level_str(self):
        return self.LEVEL.split('_')[1][:4]

    @property
    def check_name(self):
        res = getattr(self, '_check_name', None)
        if res is not None:
            return res
        return self.__traceback__.tb_next.tb_frame.f_code.co_name

    @property
    def src_file_name(self):
        assert(isinstance(self.src_line, (AllSourceLine, SourceFile)))
        if isinstance(self.src_line, AllSourceLine):
            return self.src_line.source_file.file_name

        if isinstance(self.src_line, SourceFile):
            return self.src_line.file_name

        return ''


class CheckExceptionList(Exception):

    def __init__(self):
        super().__init__()
        self._exceptions = []

    def __iter__(self):
        for e in self._exceptions:
            yield e

    def raise_append(self, exception):
        assert(isinstance(exception, ICheckException))
        self._exceptions.append(exception)

    def raise_if_any(self):
        if len(self._exceptions) > 0:
            raise self

    @contextmanager
    def context(self):
        try:
            yield self
        finally:
            self.raise_if_any()

    @contextmanager
    def check(self):
        try:
            yield self
        except ICheckException as e:
            self.raise_append(e)


class CheckError(ICheckException):
    LEVEL = '90_ERROR'


class CheckWarning(ICheckException):
    LEVEL = '50_WARNING'


class CheckInfo(ICheckException):
    LEVEL = '10_INFO'


__all__ = ['ICheckException', 'CheckExceptionList', 'CheckError', 'CheckWarning', 'CheckInfo']
