def getIntFromDict(d: dict, key: str, defaultValue: int = None):
    if d is None:
        raise ValueError(f'd argument is malformed: \"{d}\"')
    elif key is None or len(key) == 0 or key.isspace():
        raise ValueError(f'key argument is malformed: \"{key}\"')

    value = None

    if key in d and d[key] is not None:
        value = d[key]
    elif defaultValue is not None:
        value = defaultValue
    else:
        raise KeyError(f'key \"{key}\" doesn\'t exist in d: \"{d}\"')

    return int(value)

def getStrFromDict(d: dict, key: str, defaultValue: str = None, clean: bool = False):
    if d is None:
        raise ValueError(f'd argument is malformed: \"{d}\"')
    elif key is None or len(key) == 0 or key.isspace():
        raise ValueError(f'key argument is malformed: \"{key}\"')

    value = None

    if key in d and d[key] is not None:
        value = d[key]
    elif defaultValue is not None:
        value = defaultValue
    else:
        raise KeyError(f'key \"{key}\" doesn\'t exist in d: \"{d}\"')

    value = str(value)

    if clean:
        value = value.replace('\r\n', ' ').replace(
            '\r', ' ').replace('\n', ' ').strip()

    return value
