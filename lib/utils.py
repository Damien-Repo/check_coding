import os
import sys
import importlib


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class PluginManager(metaclass=Singleton):

    def __init__(self):
        self._plugins = {}

    def _load_plugins(self, plugin_cls: type, plugins_folder: str = '', prefix: str = '',
                      whitelist=None, blacklist=None) -> None:
        root_path = os.path.dirname(os.path.realpath(__file__))
        plugin_path = os.path.join(os.path.dirname(root_path), plugins_folder)

        for subFolderRoot, foldersWithinSubFolder, files in os.walk(plugin_path):
            for file in files:
                if not os.path.basename(file).endswith('.py') or not os.path.basename(file).startswith(prefix):
                    continue

                module_directory = os.path.join(plugins_folder, os.path.splitext(file)[0])
                module_str = module_directory.replace(os.path.sep, '.')
                module = importlib.import_module(module_str)

                for name in dir(module):
                    if (whitelist is not None and name not in whitelist) or \
                            (blacklist is not None and name in blacklist):
                        continue
                    cls = getattr(module, name)
                    if isinstance(cls, type) and issubclass(cls, plugin_cls) and cls != plugin_cls:
                        key = getattr(cls, 'NAME', name)
                        try:
                            self._plugins[key] = cls()
                        except AssertionError as e:
                            print(f'\nWarning: failed to load plugin "{key}" as {plugin_cls.__name__} ({e})',
                                  file=sys.stderr)

    def __getattr__(self, item):
        return self._plugins[item]

    def __getitem__(self, item):
        return self._plugins[item]

    def __len__(self):
        return len(self._plugins)

    def __iter__(self):
        for name, plugin in self._plugins.items():
            yield name, plugin
