from ..iconfig import IConfigLoader


class ConfigLoaderStr(IConfigLoader):
    DUMP_MODE = 'str'

    @classmethod
    def dump(cls, conf):
        def _rec(data: dict, indent=0):
            out = f'{" " * indent}{list(data.keys())[0]}:\n'
            for members in data.values():
                for k, v in members.items():
                    if isinstance(v, dict):
                        out += _rec({k: v}, indent + 1)
                    else:
                        out += f'{" " * indent} - {k} = {repr(v)}\n'
            return out
        return _rec(conf.dump_data())[:-1]  # [:-1] to remove useless last '\n'
