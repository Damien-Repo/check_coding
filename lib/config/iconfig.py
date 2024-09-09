import inspect


class _CustomSubClass:
    @classmethod
    def get(cls, item, default=None):
        return getattr(cls, item, default)


class IConfigLoader:
    DUMP_MODE = None

    @classmethod
    def check_type(cls, conf_file):
        if conf_file is None or conf_file == '':
            return True

    @classmethod
    def load_from_file(cls, conf_file):
        assert(cls.check_type(conf_file))
        return None

    @classmethod
    def dump(cls, conf):
        return None


class IConfig:

    @classmethod
    def load_from_data(cls, force=False, **kwargs):
        #print('LOAD DATA', force)
        #print(cls.dump_data())

        def _rec(cur_cls, params: dict):
            for k, v in params.items():
                cur_value = getattr(cur_cls, k, None)
                if isinstance(cur_value, type) and isinstance(v, dict):
                    _rec(cur_value, v)
                elif cur_value is None and isinstance(v, dict):
                    new_cls = type(k, (_CustomSubClass, ), {})
                    if force or not getattr(cur_cls, k, False):
                        setattr(cur_cls, k, new_cls)
                    _rec(new_cls, v)
                else:
                    if force or not getattr(cur_cls, k, False):
                        #print(cur_cls, k, v)
                        setattr(cur_cls, k, v)

        if cls.__name__ in kwargs:
            kwargs = kwargs[cls.__name__]
        _rec(cls, kwargs)

    @classmethod
    def init_from_data(cls, **kwargs):
        cls.load_from_data(force=True, **kwargs)

    @classmethod
    def dump_data(cls):
        def _rec(cur_cls, indent=0):
            out = {}
            for member in sorted(inspect.getmembers(cur_cls), key=lambda m: m[0]):
                if member[0].startswith('_') or \
                        inspect.ismethod(member[1]):
                    continue
                if inspect.isclass(member[1]):
                    out[member[0]] = _rec(member[1], indent + 1)
                else:
                    out[member[0]] = member[1]
            return out
        return {cls.__name__: _rec(cls)}
