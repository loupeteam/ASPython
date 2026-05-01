"""Misc utilities."""


def toDict(obj, classkey=None):
    if isinstance(obj, dict):
        return {k: toDict(v, classkey) for k, v in obj.items()}
    if hasattr(obj, "_ast"):
        return toDict(obj._ast())
    if hasattr(obj, "__iter__") and not isinstance(obj, str):
        return [toDict(v, classkey) for v in obj]
    if hasattr(obj, "__dict__"):
        data = {
            key: toDict(value, classkey)
            for key, value in obj.__dict__.items()
            if not callable(value) and not key.startswith('_')
        }
        if classkey is not None and hasattr(obj, "__class__"):
            data[classkey] = obj.__class__.__name__
        return data
    return obj
