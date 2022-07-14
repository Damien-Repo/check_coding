from lib.config import Config

from loaders import LoaderManager


class SourceFilePos:

    def __init__(self, line_start=0, col_start=0, line_end=0, col_end=0):
        self.line_start = line_start
        self.col_start = col_start
        self.line_end = line_end
        self.col_end = col_end

    def __str__(self):
        return f'<{self.line_start}:{self.col_start}->{self.line_end}:{self.col_end}>'

    @property
    def line_start(self):
        return self._line_start

    @line_start.setter
    def line_start(self, value):
        self._line_start = int(value)
        if self.line_end == 0:
            self.line_end = value

    @property
    def line_end(self):
        return getattr(self, '_line_end', 0)

    @line_end.setter
    def line_end(self, value: int):
        self._line_end = int(value) if value > self.line_start else self.line_start

    @property
    def line_str(self):
        if self.line_start < self.line_end:
            return f'[{self.line_start}-{self.line_end}]'
        return f'{self.line_start}'


class ISourceALine:
    pass


class AllSourceLine:

    def __init__(self, file_name, row, loaders):
        self._file_name = file_name
        self._row = row
        self._loaders = loaders
        self._line = {}
        for loader_name, loader in self._loaders:
            self._line[loader_name] = loader[self._row]

    def __getitem__(self, item):
        return self._line[item]

    def __getattr__(self, item):
        return self[item]

    @property
    def file_name(self):
        return self._file_name

    @property
    def row(self):
        return self._row

    def get_rel(self, offset: int):
        return self.__class__(self.file_name, self.row + offset, self._loaders)

    def next(self):
        return self.get_rel(1)

    def prev(self):
        return self.get_rel(-1)


class SourceFile:

    def __init__(self, file):
        self.file = file
        self._loaders = LoaderManager()
        self._loaders.load_file(self.file)

    @property
    def file_name(self):
        return self.file.name

    @property
    def loaders(self):
        return self._loaders

    def __str__(self):
        return self.file_name

    def __getattr__(self, item):
        return getattr(self._loaders, item)

    def __getitem__(self, item):
        return AllSourceLine(self.file_name, item, self._loaders)

    def __len__(self):
        return len(self.raw)

    def __iter__(self):
        for row, _ in enumerate(self.raw, start=1):
            line = AllSourceLine(self.file_name, row, self._loaders)
            yield line
