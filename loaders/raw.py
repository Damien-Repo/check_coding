#!/usr/bin/env python

from .loader import Loader, ILoaderLine


class LoaderLineRaw(ILoaderLine):

    def __str__(self):
        return self.line.replace('\n', '')


class LoaderRaw(Loader):

    LOADER_LINE = LoaderLineRaw
    REMOVE_EMPTY_LINE = False

    def _parse(self):
        with open(self.file_name, 'r') as f:
            for line in f.readlines():
                self.append_line(line)


if __name__ == '__main__':
    pass
