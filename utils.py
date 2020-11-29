def getIntFromDict(d: dict, key: str):
    if d == None:
        raise ValueError(f'd argument is malformed: \"{d}\"')
    elif key == None or len(key) == 0 or key.isspace():
        raise ValueError(f'key argument is malformed: \"{key}\"')
    elif key not in d:
        raise KeyError(f'key \"{key}\" doesn\'t exist in d: \"{d}\"')

    value = d[key]
    return int(value)

def getStrFromDict(d: dict, key: str, clean: bool = False):
    if d == None:
        raise ValueError(f'd argument is malformed: \"{d}\"')
    elif key == None or len(key) == 0 or key.isspace():
        raise ValueError(f'key argument is malformed: \"{key}\"')
    elif key not in d:
        raise KeyError(f'key \"{key}\" doesn\'t exist in d: \"{d}\"')

    value = d[key]
    value = str(value)

    if clean:
        value = value.replace('\r\n', ' ').replace('\r', ' ').replace('\n', ' ').strip()

    return value
