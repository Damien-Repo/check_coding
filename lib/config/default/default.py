from ..iconfig import IConfig


class DefaultConfig(IConfig):
    CUSTOM_ROOT_PATH = 'custom'

    class FileTypes:
        WHITELIST = [
            'default.*',
        ]
        BLACKLIST = []

    class Loader:
        WHITELIST = [
            'default.*',
        ]
        BLACKLIST = []

        class Clang:
            LIB_PATH = None

        class Raw:
            TAB_SIZE = None

    class Outcome:
        WHITELIST = [
            'default.OutcomeTqdm',
        ]
        BLACKLIST = []

    class Checker:
        WHITELIST = [
            'default.*',
        ]
        BLACKLIST = []
