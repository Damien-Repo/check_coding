from lib.config import DefaultConfig as C


class ConfigExample(C):
    C.Loader.Clang.LIB_PATH = '/usr/lib/llvm-10/lib/libclang.so.1'
    C.Loader.Raw.TAB_SIZE = 8

    C.Outcome.Tqdm.PrintColors.none = '\x1B[0m'
    C.Outcome.Tqdm.PrintColors.level = {
        'ERRO': '\x1B[37;41m',
        'WARN': '\x1B[37;43m',
        'INFO': '\x1B[37;46m',
    }
    C.Outcome.Tqdm.PrintColors.src_file_name = '\x1B[34;1m'
    C.Outcome.Tqdm.PrintColors.line = '\x1B[33;1m'
    C.Outcome.Tqdm.PrintColors.checker_name = '\x1B[36;1m'
    C.Outcome.Tqdm.PrintColors.check_name = '\x1B[36;1m'
    C.Outcome.Tqdm.PrintColors.message = '\x1B[31;1m'
    C.Outcome.Tqdm.PrintColors.src_line = ''
    C.Outcome.Tqdm.PrintColors.src_line_error = '\x1B[31m'
