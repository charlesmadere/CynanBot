def getIntFromDict(d: dict, key: str, fallback: int = None):
    if d is None:
        raise ValueError(f'd argument is malformed: \"{d}\"')
    elif key is None or len(key) == 0 or key.isspace():
        raise ValueError(f'key argument is malformed: \"{key}\"')

    value = None

    if key in d and d[key] is not None:
        value = d[key]
    elif fallback is not None:
        value = fallback
    else:
        raise KeyError(f'there is no fallback and key \"{key}\" doesn\'t exist in d: \"{d}\"')

    if not isinstance(value, int):
        value = int(value)

    return value

def getStrFromDict(d: dict, key: str, fallback: str = None, clean: bool = False):
    if d is None:
        raise ValueError(f'd argument is malformed: \"{d}\"')
    elif key is None or len(key) == 0 or key.isspace():
        raise ValueError(f'key argument is malformed: \"{key}\"')
    elif clean is None:
        raise ValueError(f'clean argument is malformed: \"{clean}\"')

    value = None

    if key in d and d[key] is not None:
        value = d[key]
    elif fallback is not None:
        value = fallback
    else:
        raise KeyError(f'there is no fallback and key \"{key}\" doesn\'t exist in d: \"{d}\"')

    if not isinstance(value, str):
        value = str(value)

    if clean:
        value = value.replace('\r\n', ' ').replace('\r', ' ').replace('\n', ' ').strip()

    return value
