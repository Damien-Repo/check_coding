from .iconfig import IConfig


class DefaultConfig(IConfig):
    CUSTOM_ROOT_PATH = 'custom'

    class Loader:
        class Clang:
            LIB_PATH = None

        class Raw:
            TAB_SIZE = None

    class Outcome:
        class Tqdm:
            class PrintColors:
                none = ''
                level = {
                    'ERRO': '',
                    'WARN': '',
                    'INFO': '',
                }
                src_file_name = ''
                line = ''
                checker_name = ''
                check_name = ''
                message = ''
                src_line = ''
                src_line_error = ''

    class Checker:
        pass
