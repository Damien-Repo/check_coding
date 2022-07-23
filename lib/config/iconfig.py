import inspect


class IConfig:
    @classmethod
    def init_from_data(cls, **kwargs):
        def _rec(cur_cls, params: dict):
            for k, v in params.items():
                cur_value = getattr(cur_cls, k, None)
                if isinstance(cur_value, type) and isinstance(v, dict):
                    _rec(cur_value, v)
                elif cur_value is None and isinstance(v, dict):
                    new_cls = type(k, (object, ), {})
                    setattr(cur_cls, k, new_cls)
                    _rec(new_cls, v)
                else:
                    setattr(cur_cls, k, v)

        if cls.__name__ in kwargs:
            kwargs = kwargs[cls.__name__]
        _rec(cls, kwargs)

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
