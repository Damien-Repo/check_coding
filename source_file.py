#!/usr/bin/env python

from loaders import *


class ISourceALine:
    pass


class AllSourceLine:

    def __init__(self, row, **loaders):
        self._row = row
        self._line = {}
        for loader_name, loader in loaders.items():
            self._line[loader_name] = loader[self._row]

    def __getitem__(self, item):
        return self._line[item]

    def __getattr__(self, item):
        return self[item]

    @property
    def row(self):
        return self._row


class SourceFile:

    def __init__(self, file_name):
        self._file_name = file_name
        self._loaders = {
            'raw': LoaderRaw(file_name),
            'pp': LoaderPP(file_name),
            'pp_comment': LoaderPPKeepComment(file_name),
        }

    def __str__(self):
        return self._file_name

    @property
    def raw(self):
        return self._loaders['raw']

    def __len__(self):
        return len(self.raw)

    def __iter__(self):
        for row in range(len(self)):
            line = AllSourceLine(row, **self._loaders)
            yield line

    def parse(self):
        pass


if __name__ == '__main__':
    pass