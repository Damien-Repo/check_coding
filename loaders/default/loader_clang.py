import clang.cindex

from loaders.iloader import ILoader, ILoaderLine
from lib.config import Config


class LoaderLineASTClang(ILoaderLine):

    def __str__(self):
        return str(self.line)


class LoaderASTClang(ILoader):
    NAME = 'ast'
    LOADER_LINE = LoaderLineASTClang
    REMOVE_EMPTY_LINE = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert(self.config.Loader.Clang.LIB_PATH is not None), 'Config.Loader.Clang.LIB_PATH should be set'
        clang.cindex.Config.set_library_file(self.config.Loader.Clang.LIB_PATH)

    def _parse(self):
        index = clang.cindex.Index.create()
        tu = index.parse(self.file_name, args=())
        root = tu.cursor
        all_nodes = [n for n in root.walk_preorder() if n.location.file and n.location.file.name == self.file_name]
        for n in all_nodes:
            self.append_line(n, line_num=n.location.line)
