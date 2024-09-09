import os.path
import clang.cindex

from lib.loaders.iloader import ILoader, ILoaderLine
from lib.config import Config


class LoaderLineASTClang(ILoaderLine):

    def __str__(self):
        print(f'************** {dir(self.line)}')
        for k,v in self.line.__dict__.items():
            print(f'{k}: {v}')
        print(f'**************')
        return str(self.line)

    @property
    def cursor(self):
        return self.line


class LoaderASTClang(ILoader):
    NAME = 'ast'
    LOADER_LINE = LoaderLineASTClang
    REMOVE_EMPTY_LINE = False

    EXTRA_KEY_ROOT = 'root'

    @staticmethod
    def check_by_function(src):
        #//TEMP voir pour rajouter un parametre du genre "prototype=False" pour ne lister que les proto de func
        filter = lambda x: x.kind.name == 'FUNCTION_DECL' and x.is_definition()
        # print(f'------- {src.extra[0][LoaderASTClang.NAME][LoaderASTClang.EXTRA_KEY_ROOT]} -------')
        root = src.extra[0][LoaderASTClang.NAME][LoaderASTClang.EXTRA_KEY_ROOT]
        all_functions = (x for x in root.walk_preorder() if filter(x))
        for cursor in all_functions:
            # print(f'>>>>>> check_by_function: {cursor} {src[cursor.location.line]}')
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

    def _parse(self, file, target):
        index = clang.cindex.Index.create()
        # print(f'>>>> AST: parse {file.name}')
        tu = index.parse(file.name, args=())
        root = tu.cursor
        # print(f'>>>>> ROOT: {root} ({id(self)})')
        all_nodes = [node for node in root.walk_preorder() if node.location.file and node.location.file.name == file.name]
        for cur_node in all_nodes:
            self.append_line(cur_node, target, line_number=cur_node.location.line)

        self.add_line_extra_data(target, {self.EXTRA_KEY_ROOT: root})
