
class ILoaderLine:

    def __init__(self, line):
        self._line = line

    def __len__(self):
        return len(self.line)

    def __str__(self):
        return self.line

    def __repr__(self):
        return f'{self}'

    @property
    def line(self):
        return self._line


class LoaderLineDefault(ILoaderLine):
    pass


class ILoader:
    NAME = None
    LOADER_LINE = LoaderLineDefault
    REMOVE_EMPTY_LINE = True

    CHECK_BY = {}

    def __init__(self):
        self.file = None
        self._data = {}
        self._extra = {}

    @property
    def file_name(self):
        return self.file.name

    def append_line(self, line, target, line_number=None):
        if self.REMOVE_EMPTY_LINE and not line.strip():
            return
        loaded_line = self.LOADER_LINE(line)
        # if line_num is None:
        #     line_num = len(self._data) + 1
        # line_num = int(line_num)
        # if line_num not in self._data:
        #     self._data[line_num] = []
        # self._data[line_num].append(loader_line)
        target.add_loaded_line(self.NAME, loaded_line, line_number)

    def add_line_extra_data(self, target, data, line_number=0):
        target.add_line_extra_data(self.NAME, line_number, data)

    def parse(self, file, target):
        #self.file = file
        #self._data = {}
        #self._extra = {}
        self._parse(file, target)

    @property
    def all_content(self):
        data = []
        for _, lines in self:
            for line in lines:
                data.append(line.line)
        return ''.join(data)

    def _parse(self, file, target):
        raise NotImplementedError

    def __len__(self):
        return len(self._data)

    def __getitem__(self, line_num):
        # print(f'--- {self.file_name}: {self._data}')
        return self._data.get(line_num, [])

    def __iter__(self):
        for line_num, line in sorted(self._data.items()):
            yield line_num, line
