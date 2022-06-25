from loaders.iloader import ILoader, ILoaderLine


class LoaderLineRaw(ILoaderLine):

    def __str__(self):
        return self.line.replace('\n', '')


class LoaderRaw(ILoader):
    NAME = 'raw'
    LOADER_LINE = LoaderLineRaw
    REMOVE_EMPTY_LINE = False

    def _parse(self):
        with open(self.file_name, 'r') as f:
            for line in f.readlines():
                self.append_line(line)

    def __getitem__(self, line_num):
        return super().__getitem__(line_num)[0]
