import html
import math
import os
import random
import re
from datetime import datetime
from typing import (Any, Dict, Generator, List, Optional, Pattern, Sized,
                    TypeVar, overload)
from urllib.parse import urlparse

from typing_extensions import TypeGuard


def areAllStrsInts(l: List[str]) -> bool:
    if not hasItems(l):
        raise ValueError(f'l argument is malformed: \"{l}\"')

    for s in l:
        try:
            number = int(s)

            if not isValidNum(number):
                return False
        except (SyntaxError, TypeError, ValueError):
            return False

    return True

def areValidBools(l: Optional[List[Optional[bool]]]) -> TypeGuard[List[bool]]:
    if not hasItems(l):
        return False

    for b in l:
        if not isValidBool(b):
            return False

    return True

def areValidStrs(l: Optional[List[Optional[str]]]) -> TypeGuard[List[str]]:
    if not hasItems(l):
        return False

    for s in l:
        if not isValidStr(s):
            return False

    return True

def boolToNum(b: bool) -> int:
    if not isValidBool(b):
        raise ValueError(f'b argument is malformed: \"{b}\"')

    if b:
        return 1
    else:
        return 0

def cleanPath(path: str) -> str:
    if not isValidStr(path):
        raise ValueError(f'path argument is malformed: \"{path}\"')

    return os.path.normcase(os.path.normpath(path))

carrotRemovalRegEx: Pattern = re.compile(r'<\/?\w+>', re.IGNORECASE)

def cleanStr(
    s: Optional[str],
    replacement: str = ' ',
    htmlUnescape: bool = False,
    removeCarrots: bool = False
) -> str:
    if replacement is None:
        raise ValueError(f'replacement argument is malformed: \"{replacement}\"')
    if not isValidBool(htmlUnescape):
        raise ValueError(f'htmlUnescape argument is malformed: \"{htmlUnescape}\"')
    if not isValidBool(removeCarrots):
        raise ValueError(f'removeCarrots argument is malformed: \"{removeCarrots}\"')

    if s is None:
        return ''

    s = s.replace('\r\n', replacement)\
            .replace('\r', replacement)\
            .replace('\n', replacement)\
            .strip()

    if htmlUnescape:
        s = html.unescape(s)

    if removeCarrots:
        s = carrotRemovalRegEx.sub('', s)

    return s

def containsUrl(s: Optional[str]) -> TypeGuard[str]:
    if not isValidStr(s):
        return False

    splits = s.split()

    if not hasItems(splits):
        return False

    for split in splits:
        if isValidUrl(split):
            return True

    return False

def copyList(l: List[Any]) -> List:
    newList = list()

    if hasItems(l):
        newList.extend(l)

    return newList

def cToF(celsius: float) -> float:
    if not isValidNum(celsius):
        raise ValueError(f'celsius argument is malformed: \"{celsius}\"')

    return (celsius * (9 / 5)) + 32

def formatTime(time) -> str:
    if time is None:
        raise ValueError(f'time argument is malformed: \"{time}\"')

    return time.strftime("%A, %b %d, %Y %I:%M%p")

def formatTimeShort(time, includeSeconds: bool = False) -> str:
    if time is None:
        raise ValueError(f'time argument is malformed: \"{time}\"')
    if not isValidBool(includeSeconds):
        raise ValueError(f'includeSeconds argument is malformed: \"{includeSeconds}\"')

    if includeSeconds:
        return time.strftime("%b %d %I:%M:%S%p")
    else:
        return time.strftime("%b %d %I:%M%p")

def getBoolFromDict(d: Optional[Dict[str, Any]], key: str, fallback: Optional[bool] = None) -> bool:
    if not isValidStr(key):
        raise ValueError(f'key argument is malformed: \"{key}\"')
    if fallback is not None and not isValidBool(fallback):
        raise ValueError(f'fallback argument is malformed: \"{fallback}\"')

    value: Optional[bool] = None

    if not hasItems(d):
        if fallback is None:
            raise ValueError(f'there is no fallback for key \"{key}\" and d is None/empty: \"{d}\"')
        else:
            value = fallback
    elif key in d and d[key] is not None:
        value = d[key]
    elif fallback is not None:
        value = fallback
    else:
        raise KeyError(f'there is no fallback and key \"{key}\" doesn\'t exist in d: \"{d}\"')

    if not isValidBool(value):
        if isinstance(value, (float, int)):
            value = numToBool(value)
        elif isinstance(value, str):
            value = strToBool(value)

    if not isValidBool(value):
        raise RuntimeError(f'value \"{value}\" for key \"{key}\" is malformed in d: \"{d}\"')

    return value

def getCleanedSplits(s: Optional[str]) -> List[str]:
    splits: List[str] = list()

    if not isValidStr(s):
        return splits

    words = s.split()

    if splits is None or len(splits) == 0:
        return words

    for split in splits:
        split = cleanStr(split)

        if isValidStr(split):
            words.append(split)

    return words

digitsAfterDecimalRegEx: Pattern = re.compile(r'^(\d{4}.+T.+)\.\d+(.+)$', re.IGNORECASE)
endsWithZRegEx: Pattern = re.compile(r'^(\d{4}.+T.+)Z$', re.IGNORECASE)
endsWithZAndPlusRegEx: Pattern = re.compile(r'^(\d{4}.+T.+)Z\+\d{1,2}\:\d{2}$', re.IGNORECASE)
naiveTimeZoneRegEx: Pattern = re.compile(r'^\d{4}.+T.+\:\d{1,2}\:\d{2}$', re.IGNORECASE)

def getDateTimeFromStr(text: Optional[str]) -> Optional[datetime]:
    if not isValidStr(text):
        return None

    digitsAfterDecimalMatch = digitsAfterDecimalRegEx.fullmatch(text)
    if digitsAfterDecimalMatch is not None:
        text = f'{digitsAfterDecimalMatch.group(1)}{digitsAfterDecimalMatch.group(2)}'

    endsWithZMatch = endsWithZRegEx.fullmatch(text)
    if endsWithZMatch is not None:
        text = endsWithZMatch.group(1)
    else:
        endsWithZAndPlusMatch = endsWithZAndPlusRegEx.fullmatch(text)

        if endsWithZAndPlusMatch is not None:
            text = endsWithZAndPlusMatch.group(1)

    if naiveTimeZoneRegEx.fullmatch(text) is not None:
        text = f'{text}+00:00'

    return datetime.fromisoformat(text)

def getFloatFromDict(d: Optional[Dict[str, Any]], key: str, fallback: Optional[float] = None) -> float:
    if not isValidStr(key):
        raise ValueError(f'key argument is malformed: \"{key}\"')
    if fallback is not None and not isValidNum(fallback):
        raise ValueError(f'fallback argument is malformed: \"{fallback}\"')

    value: Optional[float] = None

    if not hasItems(d):
        if fallback is None:
            raise ValueError(f'there is no fallback for key \"{key}\" and d is None/empty: \"{d}\"')
        else:
            value = fallback
    elif key in d and d[key] is not None:
        value = d[key]
    elif fallback is not None:
        value = fallback
    else:
        raise KeyError(f'there is no fallback and key \"{key}\" doesn\'t exist in d: \"{d}\"')

    if not isinstance(value, float):
        value = float(value)

    if not isValidNum(value):
        raise ValueError(f'value \"{value}\" for key \"{key}\" is malformed in d: \"{d}\"')

    return value

def getIntFromDict(d: Optional[Dict[str, Any]], key: str, fallback: Optional[int] = None) -> int:
    if not isValidStr(key):
        raise ValueError(f'key argument is malformed: \"{key}\"')
    if fallback is not None and not isValidNum(fallback):
        raise ValueError(f'fallback argument is malformed: \"{fallback}\"')

    value: Optional[int] = None

    if not hasItems(d):
        if fallback is None:
            raise ValueError(f'there is no fallback for key \"{key}\" and d is None/empty: \"{d}\"')
        else:
            value = fallback
    elif key in d and d[key] is not None:
        value = d[key]
    elif fallback is not None:
        value = fallback
    else:
        raise KeyError(f'there is no fallback and key \"{key}\" doesn\'t exist in d: \"{d}\"')

    if not isinstance(value, int):
        value = int(value)

    if not isValidInt(value):
        raise ValueError(f'value \"{value}\" for key \"{key}\" is malformed in d: \"{d}\"')

    return value

def getIntMaxSafeSize() -> int:
    # Taken from Java's Integer.MAX_VALUE constant.
    return 2147483647

def getIntMinSafeSize() -> int:
    # Taken from Java's Integer.MIN_VALUE constant.
    return -2147483648

def getLongMaxSafeSize() -> int:
    # Taken from Java's Long.MAX_VALUE constant. This seems to also be exactly identical to
    # SQLite's maximum INTEGER size (8 bytes, signed).
    return 9223372036854775807

def getLongMinSafeSize() -> int:
    # Taken from Java's Long.MIN_VALUE constant. This seems to also be exactly identical to
    # SQLite's minimum INTEGER size (8 bytes, signed).
    return -9223372036854775808

def getRandomSadEmoji() -> str:
    sadEmoji: List[str] = [ '😭', '😢', '😿', '🤣', '😥', '🥲' ]
    return random.choice(sadEmoji)

def getRandomSpaceEmoji() -> str:
    spaceEmoji: List[str] = [ '🚀', '👾', '☄️', '🌌', '👨‍🚀', '👩‍🚀', '👽', '🌠' ]
    return random.choice(spaceEmoji)

def getStrFromDict(
    d: Optional[Dict[str, Any]],
    key: str,
    fallback: Optional[str] = None,
    clean: bool = False,
    htmlUnescape: bool = False,
    removeCarrots: bool = False
) -> str:
    if not isValidStr(key):
        raise ValueError(f'key argument is malformed: \"{key}\"')
    assert fallback is None or isinstance(fallback, str), f"malformed {fallback=}"
    if not isValidBool(clean):
        raise ValueError(f'clean argument is malformed: \"{clean}\"')
    if not isValidBool(htmlUnescape):
        raise ValueError(f'htmlUnescape argument is malformed: \"{htmlUnescape}\"')
    if not isValidBool(removeCarrots):
        raise ValueError(f'removeCarrots argument is malformed: \"{removeCarrots}\"')

    value: Optional[str] = None

    if not hasItems(d):
        if fallback is None:
            raise ValueError(f'there is no fallback for key \"{key}\" and d is None/empty: \"{d}\"')
        else:
            value = fallback
    elif key in d and d[key] is not None:
        value = d[key]
    elif fallback is not None:
        value = fallback
    else:
        raise KeyError(f'there is no fallback and key \"{key}\" doesn\'t exist in d: \"{d}\"')

    if not isinstance(value, str):
        value = str(value)

    if clean:
        value = cleanStr(value, htmlUnescape = htmlUnescape, removeCarrots = removeCarrots)

    return value

T_Sized = TypeVar("T_Sized", bound=Sized)

def hasItems(l: Optional[T_Sized]) -> TypeGuard[T_Sized]:
    return l is not None and len(l) >= 1

def isValidBool(b: Optional[bool]) -> TypeGuard[bool]:
    return b is not None and isinstance(b, bool)

def isValidInt(i: Optional[float]) -> TypeGuard[int]:
    return isValidNum(i) and isinstance(i, int)

def isValidNum(n: Optional[float]) -> TypeGuard[float]:
    return n is not None and isinstance(n, (float, int)) and math.isfinite(n)

def isValidStr(s: Optional[str]) -> TypeGuard[str]:
    """ str len >= 1, not all space """
    return s is not None and isinstance(s, str) and len(s) >= 1 and not s.isspace()

def isValidUrl(s: Optional[str]) -> TypeGuard[str]:
    if not isValidStr(s):
        return False

    parsed = urlparse(s)

    if isValidStr(parsed.scheme) and isValidStr(parsed.netloc):
        url = parsed.geturl()
        return isValidStr(url)

    return False

def numToBool(n: Optional[float]) -> bool:
    if not isValidNum(n):
        raise ValueError(f'n argument is malformed: \"{n}\"')

    return n != 0

def permuteSubArrays(array: List[Any], pos: int = 0) -> Generator[List[Any], None, None]:
    if not isValidNum(pos):
        raise ValueError(f'pos argument is malformed: \"{pos}\"')

    if pos >= len(array):
        yield []
    elif all(not isinstance(item, list) for item in array):
        for item in array:
            yield [item]
    elif isinstance(array[pos], list):
        for subArray in permuteSubArrays(array[pos]):
            for nextSubArray in permuteSubArrays(array, pos + 1):
                yield subArray + list(nextSubArray)
    else:
        for subArray in permuteSubArrays(array, pos + 1):
            yield [array[pos]] + list(subArray)

def randomBool() -> bool:
    return bool(random.getrandbits(1))

@overload
def removePreceedingAt(s: None) -> None:
    ...
@overload
def removePreceedingAt(s: str) -> str:
    ...

def removePreceedingAt(s: Optional[str]) -> Optional[str]:
    if s is None:
        return s
    if s.startswith("@"):
        return s[1:]
    return s

def splitLongStringIntoMessages(
    maxMessages: int,
    perMessageMaxSize: int,
    message: Optional[str]
) -> List[str]:
    if not isValidInt(maxMessages):
        raise ValueError(f'maxMessages argument is malformed: \"{maxMessages}\"')
    if maxMessages < 1 or maxMessages >= getIntMaxSafeSize():
        raise ValueError(f'maxMessages argument is out of bounds: {maxMessages}')
    if not isValidInt(perMessageMaxSize):
        raise ValueError(f'perMessageMaxSize argument is malformed: \"{perMessageMaxSize}\"')
    if perMessageMaxSize < 50 or perMessageMaxSize >= getIntMaxSafeSize():
        raise ValueError(f'perMessageMaxSize argument is out of bounds: {perMessageMaxSize}')

    messages: List[str] = list()

    if not isValidStr(message):
        return messages

    messages.append(message)
    index: int = 0

    while index < len(messages):
        m = messages[index]

        if len(m) >= perMessageMaxSize:
            spaceIndex = m.rfind(' ')

            while spaceIndex >= perMessageMaxSize:
                spaceIndex = m[0:spaceIndex].rfind(' ')

            if spaceIndex == -1:
                raise RuntimeError(f'This message is insane! (len is {len(message)}):\n{message}')

            messages[index] = m[0:spaceIndex].strip()
            messages.append(m[spaceIndex:len(m)].strip())

        index = index + 1

    if len(messages) > maxMessages:
        raise RuntimeError(f'This message is too long! (len is {len(message)}):\n{message}')

    return messages

alphanumericRegEx: Pattern = re.compile(r'.*[a-z0-9]+.*', re.IGNORECASE)

def strContainsAlphanumericCharacters(s: Optional[str]) -> TypeGuard[str]:
    if not isValidStr(s):
        return False

    return alphanumericRegEx.match(s) is not None

trueRegEx: Pattern = re.compile(r't(rue)?|y(es)?', re.IGNORECASE)
falseRegEx: Pattern = re.compile(r'f(alse)?|n(o)?', re.IGNORECASE)

def strictStrToBool(s: Optional[str]) -> bool:
    """_summary_

    Converts the given string into a bool. None/empty/whitespace strings will cause an exception
    to be raised. Random strings ("abc123", "asdf", "qwerty", etc) will return True. Only strings
    that provide a match with falseRegEx will return False.

    Parameters
    ------------
    s: str
        The string to convert into a bool (if None, an exception will be raised)

    Raises
    --------
    ValueError
        This exception will be raised if the given string matches neither one of trueRegEx nor
        falseRegEx.
    """

    if not isValidStr(s):
        raise ValueError(f's argument is malformed: \"{s}\"')

    if trueRegEx.match(s) is not None:
        return True
    elif falseRegEx.match(s) is not None:
        return False
    else:
        raise ValueError(f'no matching bool conversion: \"{s}\"')

def strToBool(s: Optional[str]) -> bool:
    """_summary_

    Converts the given string into a bool. None/empty/whitespace strings are converted into True.
    Random strings ("abc123", "asdf", "qwerty", etc) will return True. Only strings that provide a
    match with falseRegEx will return False.

    Parameters
    ------------
    s: str
        The string to convert into a bool (can be None)
    """

    if not isValidStr(s) or falseRegEx.match(s) is None:
        return True
    else:
        return False

def strsToBools(l: Optional[List[Optional[str]]]) -> List[bool]:
    newList: List[bool] = list()

    if not hasItems(l):
        return newList

    for s in l:
        newList.append(strToBool(s))

    return newList
