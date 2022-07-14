from lib.config import Config

from loaders.iloader import ILoader, ILoaderLine


class LoaderLineRaw(ILoaderLine):

    def __str__(self):
        return self.line.replace('\n', '')

    def _clever(self, line):
        tabsize = Config().Loader.Raw.TAB_SIZE if Config().Loader.Raw.TAB_SIZE is not None else 1
        line = line.replace('\n', '')
        i = 0
        for c in line:
            out = ' ' * (tabsize - i % tabsize) if c == '\t' else c
            yield out
            i += len(out)

    @property
    def clever(self):
        return ''.join(self._clever(self.line))

    def clever_sub_str(self, start=0, end=-1):
        return ''.join(self._clever(self.line[start:end]))


class LoaderRaw(ILoader):
    NAME = 'raw'
    LOADER_LINE = LoaderLineRaw
    REMOVE_EMPTY_LINE = False

    CHECK_BY = {
        'line': lambda src: (src_line for src_line in src),
        'file': lambda src: [src],
    }

    def _parse(self):
        for line in self.file.readlines():
            self.append_line(line)

    def __getitem__(self, line_num):
        return super().__getitem__(line_num)[0]
