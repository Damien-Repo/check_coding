from lib.config import Config


class ConfigExample(Config):
    Config.Loader.Clang.LIB_PATH = '/usr/lib/llvm-10/lib/libclang.so.1'
