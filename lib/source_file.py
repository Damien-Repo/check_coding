from lib.config import Config

from loaders import LoaderManager


class ISourceALine:
    pass


class AllSourceLine:

    def __init__(self, row, loaders):
        self._row = row
        self._line = {}
        for loader_name, loader in loaders:
            self._line[loader_name] = loader[self._row]

    def __getitem__(self, item):
        return self._line[item]

    def __getattr__(self, item):
        return self[item]

    @property
    def row(self):
        return self._row


class SourceFile:

    def __init__(self, file_name, config=Config):
        self.config = config
        self._file_name = file_name
        self._loaders = LoaderManager(config=self.config)
        self._loaders.load_file(self._file_name)

    def __str__(self):
        return self._file_name

    @property
    def raw(self):
        return self._loaders.raw

    def __len__(self):
        return len(self.raw)

    def __iter__(self):
        for row, _ in enumerate(self.raw, start=1):
            line = AllSourceLine(row, self._loaders)
            yield line
