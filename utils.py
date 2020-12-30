from typing import List


def cleanStr(s: str):
    if s is None:
        raise ValueError(f's argument is malformed: \"{s}\"')

    return s.replace('\r\n', ' ').replace('\r', ' ').replace('\n', ' ').strip()

def formatTime(time):
    if time is None:
        raise ValueError(f'time argument is malformed: \"{time}\"')

    return time.strftime("%A, %b %d, %Y %I:%M%p")

def formatTimeShort(time):
    if time is None:
        raise ValueError(f'time argument is malformed: \"{time}\"')

    return time.strftime("%b %d %I:%M%p")

def getCleanedSplits(s: str):
    splits = list()

    if not isValidStr(s):
        return splits

    words = s.split()

    if splits is None or len(splits) == 0:
        return words

    for split in splits:
        if split is not None:
            split = cleanStr(split)

        if isValidStr(split):
            words.append(split)

    return words

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
    elif not isValidStr(key):
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
        value = cleanStr(value)

    return value

def isValidList(l: List):
    return l is not None and len(l) >= 1

def isValidStr(s: str):
    return s is not None and len(s) >= 1 and not s.isspace()

def removePreceedingAt(s: str):
    if not isValidStr(s):
        return s
    elif s[0] != '@':
        return s
    else:
        return s[1:len(s)]
