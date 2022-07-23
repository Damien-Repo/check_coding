import json

from . import IConfigLoader
from .default import DefaultConfig


class ConfigLoaderJSON(IConfigLoader):
    DUMP_MODE = 'json'

    @classmethod
    def check_type(cls, conf_file):
        return getattr(conf_file, 'name', False) and conf_file.name.endswith('.json')

    @classmethod
    def load_from_file(cls, conf_file):
        assert(cls.check_type(conf_file))
        data = json.loads(conf_file.read())
        name = 'JSONConfig'
        if len(data.keys()) == 1 and isinstance(list(data.values())[0], dict):
            name = list(data.keys())[0]
        else:
            name = f'Custom{name}'
            data = {name: data}
        conf = type(name, (DefaultConfig,), {})
        conf.init_from_data(**data)
        return conf

    @classmethod
    def dump(cls, conf):
        data = conf.dump_data()
        return json.dumps(data)
