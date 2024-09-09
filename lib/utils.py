import os
import sys
import importlib
import inspect


class Singleton(type):
    _instances = {}

    def __call__(cls, reset=False, *args, **kwargs):
        if reset or cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class PluginManager(metaclass=Singleton):

    def __init__(self):
        self._plugins = {}
        self.default_config = None

    @staticmethod
    def _is_allowed(name, whitelist, blacklist):
        allowed = True
        if whitelist is not None:
            l = [x for x in whitelist
                 if (x[-2:] == '.*' and name.startswith(x[:-2])) or x.startswith(name)]
            if len(l) == 0:
                # print('WL!!!!!', name, l, whitelist)
                allowed = False

        if blacklist is not None:
            l = [x for x in blacklist
                 if (x[-2:] == '.*' and name.startswith(x[:-2])) or x == name]
            if len(l) > 0:
                # print('BL!!!', name, l)
                allowed = False

        # if allowed:
        #     print(name, 'allowed:', allowed, whitelist, blacklist)
        return allowed

    def load_plugins(self, plugin_cls: type, plugins_folder: str = '', prefix: str = '',
                     whitelist=None, blacklist=None, create_plugin_instance: bool = True) -> None:
        root_path = os.path.dirname(os.path.realpath(__file__))
        plugin_path = os.path.join(os.path.dirname(root_path), plugins_folder)

        for subFolderRoot, foldersWithinSubFolder, files in os.walk(plugin_path):
            sub_folder = subFolderRoot.replace(f'{plugin_path}', '').lstrip('/')

            if '__pycache__' in sub_folder:
                continue

            normalized_sub_folder = sub_folder.replace(os.path.sep, '.')
            for file in files:
                if not os.path.basename(file).endswith('.py') or not os.path.basename(file).startswith(prefix):
                    continue

                module_directory = os.path.join(plugins_folder, sub_folder, os.path.splitext(file)[0])
                module_str = module_directory.replace(os.path.sep, '.')
                module = importlib.import_module(module_str)

                for name in [n for n, m in inspect.getmembers(module, inspect.isclass) if m.__module__ == module_str]:
                    if name.startswith(('_', 'I')):
                        continue
                    normalized_name = '.'.join([normalized_sub_folder, name]).lstrip('.')
                    if not self._is_allowed(normalized_name, whitelist, blacklist):
                        continue

                    cls = getattr(module, name)
                    self.default_config = getattr(module, '__default_config__', None)
                    if isinstance(cls, type) and issubclass(cls, plugin_cls) and cls != plugin_cls:
                        key = getattr(cls, 'NAME', None)
                        if key is None:
                            key = name
                        if create_plugin_instance:
                            try:
                                self._plugins[key] = cls()
                            except AssertionError as e:
                                print(f'\nWarning: failed to load plugin "{key}" as {plugin_cls.__name__} ({e})',
                                      file=sys.stderr)
                        else:
                            self._plugins[key] = cls

    def load_default_config(self, config):
        config.load_from_data(self.default_config)

    def __getattr__(self, item):
        return self._plugins.get(item)

    def __getitem__(self, item):
        return self._plugins[item]

    def __len__(self):
        return len(self._plugins)

    def __iter__(self):
        for name, plugin in self._plugins.items():
            yield name, plugin
