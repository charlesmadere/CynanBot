import html
import math
import os
import random
import re
from collections.abc import Collection
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

def areValidBools(l: Optional[Collection[Optional[bool]]]) -> TypeGuard[Collection[bool]]:
    if not hasItems(l):
        return False

    for b in l:
        if not isValidBool(b):
            return False

    return True

def areValidStrs(l: Optional[Collection[Optional[str]]]) -> TypeGuard[Collection[str]]:
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
extraWhiteSpaceRegEx: Pattern = re.compile(r'\s{2,}', re.IGNORECASE)

def cleanStr(
    s: str | None,
    replacement: str = ' ',
    htmlUnescape: bool = False,
    removeCarrots: bool = False
) -> str:
    if replacement is None:
        raise TypeError(f'replacement argument is malformed: \"{replacement}\"')
    elif not isValidBool(htmlUnescape):
        raise TypeError(f'htmlUnescape argument is malformed: \"{htmlUnescape}\"')
    elif not isValidBool(removeCarrots):
        raise TypeError(f'removeCarrots argument is malformed: \"{removeCarrots}\"')

    if s is None or len(s) == 0:
        return ''

    s = extraWhiteSpaceRegEx.sub(' ', s).strip()

    s = s.replace('\r\n', replacement)\
         .replace('\r', replacement)\
         .replace('\n', replacement)\
         .strip()

    if htmlUnescape:
        s = html.unescape(s)

    if removeCarrots:
        s = carrotRemovalRegEx.sub('', s)

    return s.strip()

def containsUrl(s: str | None) -> TypeGuard[str]:
    if not isValidStr(s):
        return False

    splits = s.split()

    if splits is None or len(splits) == 0:
        return False

    for split in splits:
        if isValidUrl(split):
            return True

    return False

def copyList(l: list[Any] | None) -> list:
    newList = list()

    if l is not None and len(l) >= 1:
        newList.extend(l)

    return newList

def copySet(s: set[Any] | None) -> set:
    newSet = set()

    if s is not None and len(s) >= 1:
        newSet.update(s)

    return newSet

def cToF(celsius: float) -> float:
    if not isValidNum(celsius):
        raise TypeError(f'celsius argument is malformed: \"{celsius}\"')

    return (celsius * (9.0 / 5.0)) + 32.0

def formatTime(time) -> str:
    if time is None:
        raise ValueError(f'time argument is malformed: \"{time}\"')

    return time.strftime("%A, %b %d, %Y %I:%M%p")

def formatTimeShort(time, includeSeconds: bool = False) -> str:
    if time is None:
        raise ValueError(f'time argument is malformed: \"{time}\"')
    elif not isValidBool(includeSeconds):
        raise ValueError(f'includeSeconds argument is malformed: \"{includeSeconds}\"')

    if includeSeconds:
        return time.strftime("%b %d %I:%M:%S%p")
    else:
        return time.strftime("%b %d %I:%M%p")

def getBoolFromDict(d: Optional[Dict[str, Any]], key: str, fallback: Optional[bool] = None) -> bool:
    if not isValidStr(key):
        raise ValueError(f'key argument is malformed: \"{key}\"')
    elif fallback is not None and not isValidBool(fallback):
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

def getCleanedSplits(s: str | None) -> list[str]:
    words: list[str] = list()

    if not isValidStr(s):
        return words

    splits = s.split()

    if splits is None or len(splits) == 0:
        return words

    for split in splits:
        split = cleanStr(split)

        if isValidStr(split):
            words.append(split)

    return words

def getDateTimeFromDict(
    d: dict[str, Any] | None,
    key: str,
    fallback: datetime | None = None
) -> datetime:
    if d is not None and not isinstance(d, dict):
        raise TypeError(f'd argument is malformed: \"{d}\"')
    elif not isValidStr(key):
        raise TypeError(f'key argument is malformed: \"{key}\"')
    elif fallback is not None and not isinstance(fallback, datetime):
        raise TypeError(f'fallback argument is malformed: \"{fallback}\"')

    value: datetime | None = None

    if d is None or len(d) == 0:
        if fallback is not None:
            return fallback
        else:
            raise ValueError(f'there is no fallback for key \"{key}\" and d is None/empty: \"{d}\"')

    valueString: str | None = None

    if isValidStr(d.get(key, None)):
        valueString = d[key]
    elif fallback is not None:
        value = fallback
    else:
        raise KeyError(f'there is no fallback and key \"{key}\" doesn\'t exist in d: \"{d}\"')

    if isValidStr(valueString):
        value = datetime.fromisoformat(valueString)

    if not isinstance(value, datetime):
        raise ValueError(f'there is no fallback for key \"{key}\" and d is None/empty: \"{d}\"')

    return value

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

    assert isinstance(text, str)

    return datetime.fromisoformat(text)

def getFloatFromDict(d: Optional[Dict[str, Any]], key: str, fallback: Optional[float] = None) -> float:
    if not isValidStr(key):
        raise ValueError(f'key argument is malformed: \"{key}\"')
    elif fallback is not None and not isValidNum(fallback):
        raise ValueError(f'fallback argument is malformed: \"{fallback}\"')

    value: Optional[float] = None

    if not hasItems(d):
        if isValidNum(fallback):
            value = fallback
        else:
            raise ValueError(f'there is no fallback for key \"{key}\" and d is None/empty: \"{d}\"')
    elif key in d and d[key] is not None:
        value = d[key]
    elif fallback is not None:
        value = fallback
    else:
        raise KeyError(f'there is no fallback and key \"{key}\" doesn\'t exist in d: \"{d}\"')

    if value is not None and not isinstance(value, float):
        value = float(value)

    if not isValidNum(value):
        raise ValueError(f'value \"{value}\" for key \"{key}\" is malformed in d: \"{d}\"')

    return value

def getIntFromDict(d: Optional[Dict[str, Any]], key: str, fallback: Optional[int] = None) -> int:
    if not isValidStr(key):
        raise ValueError(f'key argument is malformed: \"{key}\"')
    elif fallback is not None and not isValidNum(fallback):
        raise ValueError(f'fallback argument is malformed: \"{fallback}\"')

    value: Optional[float] = None

    if not hasItems(d):
        if isValidNum(fallback):
            value = fallback
        else:
            raise ValueError(f'there is no fallback for key \"{key}\" and d is None/empty: \"{d}\"')
    elif key in d and d[key] is not None:
        value = d[key]
    elif isValidNum(fallback):
        value = fallback
    else:
        raise KeyError(f'there is no fallback and key \"{key}\" doesn\'t exist in d: \"{d}\"')

    if value is not None and not isinstance(value, int):
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
    d: dict[str, Any] | None,
    key: str,
    fallback: str | None = None,
    clean: bool = False,
    htmlUnescape: bool = False,
    removeCarrots: bool = False
) -> str:
    if not isValidStr(key):
        raise ValueError(f'key argument is malformed: \"{key}\"')
    elif fallback is not None and not isinstance(fallback, str):
        raise ValueError(f'fallback argument is malformed: \"{fallback}\"')
    elif not isValidBool(clean):
        raise ValueError(f'clean argument is malformed: \"{clean}\"')
    elif not isValidBool(htmlUnescape):
        raise ValueError(f'htmlUnescape argument is malformed: \"{htmlUnescape}\"')
    elif not isValidBool(removeCarrots):
        raise ValueError(f'removeCarrots argument is malformed: \"{removeCarrots}\"')

    value: str | None = None

    if d is None or len(d) == 0:
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

def isValidStr(s: str | None) -> TypeGuard[str]:
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

def numToBool(n: float | None) -> bool:
    if not isValidNum(n):
        raise ValueError(f'n argument is malformed: \"{n}\"')

    return n != 0

def permuteSubArrays(array: List[Any], pos: int = 0) -> Generator[List[Any], None, None]:
    if not isValidInt(pos):
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
    elif s.startswith('@'):
        return s[1:]
    else:
        return s

def safeStrToInt(s: Optional[str]) -> Optional[int]:
    if not isValidStr(s):
        return None

    try:
        return int(s)
    except Exception:
        return None

def splitLongStringIntoMessages(
    maxMessages: int,
    perMessageMaxSize: int,
    message: Optional[str]
) -> List[str]:
    if not isValidInt(maxMessages):
        raise ValueError(f'maxMessages argument is malformed: \"{maxMessages}\"')
    elif maxMessages < 1 or maxMessages >= getIntMaxSafeSize():
        raise ValueError(f'maxMessages argument is out of bounds: {maxMessages}')
    elif not isValidInt(perMessageMaxSize):
        raise ValueError(f'perMessageMaxSize argument is malformed: \"{perMessageMaxSize}\"')
    elif perMessageMaxSize < 50 or perMessageMaxSize >= getIntMaxSafeSize():
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

def strictStrToBool(s: str | None) -> bool:
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
    TypeError
        This exception will be raised if the argument is an incorrect type.

    ValueError
        This exception will be raised if the given string matches neither one of trueRegEx nor
        falseRegEx.
    """

    if s is not None and not isinstance(s, str):
        raise TypeError(f's argument is malformed: \"{s}\"')
    elif not isValidStr(s):
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

def strsToBools(l: Collection[str] | None) -> List[bool]:
    bools: List[bool] = list()

    if not hasItems(l):
        return bools

    for s in l:
        bools.append(strToBool(s))

    return bools
