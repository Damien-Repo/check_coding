from lib.loaders import LoaderManager
from lib.loaders.default.loader_raw import LoaderRaw
from lib.filetypes import FileTypesManager


class SourceFilePos:

    def __init__(self, line_start=0, col_start=0, line_end=0, col_end=0):
        self.line_start = line_start
        self.col_start = col_start
        self.line_end = line_end
        self.col_end = col_end

    def __eq__(self, other):
        return (
            self.line_start == other.line_start and
            self.col_start == other.col_start and
            self.line_end == other.line_end and
            self.col_end == other.col_end
        )

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

    def __init__(self, source_file, loader_name, line_number, loaded_line):
        self._source_file = source_file
        self._line_number = line_number
        self._line = {
            loader_name: [loaded_line],
        }

    def __getattr__(self, loader_name):
        return self._line.get(loader_name, [])

    @property
    def line_number(self):
        return self._line_number

    @property
    def source_file(self):
        return self._source_file

    def get_rel(self, offset: int):
        return self._source_file[self._line_number + offset]

    def next(self):
        return self.get_rel(1)

    def prev(self):
        return self.get_rel(-1)

    def update_line(self, loader_name, loaded_line):
        if loader_name not in self._line:
            self._line[loader_name] = []
        self._line[loader_name].append(loaded_line)

class SourceFile:

    def __init__(self, file):
        self.file = file
        self._type = FileTypesManager().get_file_type(self.file.name)
        # self._loaders = LoaderManager()
        # self._loaders.load_file(self.file)

        self._content = []
        self._extra = {}
        self._used_loaders_name = set()

        loaders = LoaderManager()
        loaders.load_file(self.file, self)

        # for row, _ in enumerate(loaders.raw, start=1):
        #     line = AllSourceLine(self.file_name, row, loaders)
        #     self._content.append(line)

    @property
    def file_name(self):
        return self.file.name

    @property
    def type(self):
        return self._type

    @property
    def extra(self):
        return self._extra

    @property
    def all_loaders_name(self):
        return list(self._used_loaders_name)

    def __str__(self):
        return self.file_name

    def get_content(self, loader_name):
        assert(loader_name in self._used_loaders_name)
        return (''.join(map(str, getattr(line, loader_name))) for line in self._content)

    def __getitem__(self, line_number):
        assert(1 <= line_number <= len(self._content) + 1)
        # print(f'++++++ source_file: {self.file_name} => {line_number}')
        return self._content[line_number - 1]
        # return AllSourceLine(self.file_name, item, self._loaders)

    def __len__(self):
        return len(self._content)

    def __iter__(self):
        for line in self._content:
            yield line

        # for row, _ in enumerate(self.raw, start=1):
        #     line = AllSourceLine(self.file_name, row, self._loaders)
        #     yield line

    def add_loaded_line(self, loader_name, loaded_line, line_number=None):
        if line_number is None:
            line_number = len(self._content) + 1

        line_number = int(line_number)
        assert(1 <= line_number <= len(self._content) + 1)
        if line_number == len(self._content) + 1:
            self._content.append(None)

        line_index = line_number - 1

        if self._content[line_index] is None:
            self._content[line_index] = AllSourceLine(self, loader_name, line_number, loaded_line)
        else:
            self._content[line_index].update_line(loader_name, loaded_line)

        self._used_loaders_name.add(loader_name)

    def add_line_extra_data(self, loader_name: str, line_number: int, data: dict):
        if line_number not in self._extra:
            self._extra[line_number] = {}

        if loader_name not in self._extra[line_number]:
            self._extra[line_number][loader_name] = {}

        self._extra[line_number][loader_name].update(data)
