import os.path
import clang.cindex

from loaders.iloader import ILoader, ILoaderLine
from lib.config import Config


class LoaderLineASTClang(ILoaderLine):

    def __str__(self):
        return str(self.line)

    @property
    def cursor(self):
        return self.line


class LoaderASTClang(ILoader):
    NAME = 'ast'
    LOADER_LINE = LoaderLineASTClang
    REMOVE_EMPTY_LINE = False

    @staticmethod
    def check_by_function(src):
        #//TEMP voir pour rajouter un parametre du genre "prototype=False" pour ne lister que les proto de func
        filter = lambda x: x.kind.name == 'FUNCTION_DECL' and x.is_definition()
        all_functions = (x for x in src.ast.root.walk_preorder() if filter(x))
        for cursor in all_functions:
            yield src[cursor.location.line]

    CHECK_BY = {
        'function': check_by_function.__func__,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert(Config().Loader.Clang.LIB_PATH is not None), 'Config.Loader.Clang.LIB_PATH should be set'
        assert(os.path.exists(Config().Loader.Clang.LIB_PATH)), f'Config.Loader.Clang.LIB_PATH file should be exists' \
                                                                f' ("{Config().Loader.Clang.LIB_PATH}")'
        clang.cindex.Config.set_library_file(Config().Loader.Clang.LIB_PATH)

    def _parse(self):
        index = clang.cindex.Index.create()
        tu = index.parse(self.file_name, args=())
        self.root = tu.cursor
        all_nodes = [n for n in self.root.walk_preorder() if n.location.file and n.location.file.name == self.file_name]
        for n in all_nodes:
            self.append_line(n, line_num=n.location.line)
