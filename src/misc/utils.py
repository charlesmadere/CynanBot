import html
import math
import random
import re
from datetime import datetime
from typing import Any, Final, Generator, Pattern, Sized, TypeVar, overload
from urllib.parse import urlparse

from frozendict import frozendict
from frozenlist import FrozenList
from typing_extensions import TypeGuard


def areAllStrsInts(l: list[str]) -> bool:
    if not isinstance(l, list):
        raise TypeError(f'l argument is malformed: \"{l}\"')
    elif len(l) == 0:
        raise ValueError(f'l argument can\'t be empty: \"{l}\"')

    for s in l:
        try:
            number = int(s)
        except (SyntaxError, TypeError, ValueError):
            return False

        if not isValidInt(number):
            return False

    return True

def boolToInt(b: bool) -> int:
    if not isValidBool(b):
        raise TypeError(f'b argument is malformed: \"{b}\"')

    if b:
        return 1
    else:
        return 0

CARROT_REMOVAL_REG_EX: Final[Pattern] = re.compile(r'<\/?\w+>', re.IGNORECASE)
EXTRA_WHITE_SPACE_REG_EX: Final[Pattern] = re.compile(r'\s{2,}', re.IGNORECASE)
RIDICULOUS_BLANK_CHARACTERS_REG_EX: Final[Pattern] = re.compile(r'[\U000e0000]', re.IGNORECASE)

def cleanStr(
    s: str | None,
    replacement: str = ' ',
    htmlUnescape: bool = False,
    removeCarrots: bool = False,
) -> str:
    if s is not None and not isinstance(s, str):
        raise TypeError(f's argument is malformed: \"{s}\"')
    elif replacement is None:
        raise TypeError(f'replacement argument is malformed: \"{replacement}\"')
    elif not isValidBool(htmlUnescape):
        raise TypeError(f'htmlUnescape argument is malformed: \"{htmlUnescape}\"')
    elif not isValidBool(removeCarrots):
        raise TypeError(f'removeCarrots argument is malformed: \"{removeCarrots}\"')

    if s is None or len(s) == 0 or s.isspace():
        return ''

    s = EXTRA_WHITE_SPACE_REG_EX.sub(' ', s).strip()
    s = RIDICULOUS_BLANK_CHARACTERS_REG_EX.sub('', s).strip()

    s = s.replace('\r\n', replacement)\
         .replace('\r', replacement)\
         .replace('\n', replacement)\
         .strip()

    if htmlUnescape:
        s = html.unescape(s)

    if removeCarrots:
        s = CARROT_REMOVAL_REG_EX.sub('', s)

    return s.strip()

# this regex pattern is designed to match strings that Twitch automatically converts into a clickable link in Twitch chat
SHORTHAND_URL_REG_EX: Final[Pattern] = re.compile(r'^\W?\w[\w_-]*\.(?:com|co(?:\.\w{2,})?|edu|gov|io|mil|net|org)\W?$', re.IGNORECASE)

def containsUrl(s: str | None) -> TypeGuard[str]:
    if not isValidStr(s):
        return False

    splits = s.split()

    if splits is None or len(splits) == 0:
        return False

    for split in splits:
        if not isValidStr(split):
            continue
        elif isValidUrl(split) or SHORTHAND_URL_REG_EX.fullmatch(split) is not None:
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

def getBoolFromDict(d: dict[str, Any] | None, key: str, fallback: bool | None = None) -> bool:
    if d is not None and not isinstance(d, dict):
        raise TypeError(f'd argument is malformed: \"{d}\"')
    elif not isValidStr(key):
        raise TypeError(f'key argument is malformed: \"{key}\"')
    elif fallback is not None and not isValidBool(fallback):
        raise TypeError(f'fallback argument is malformed: \"{fallback}\"')

    value: bool | None = None

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

    if not isValidBool(value):
        if isinstance(value, (float, int)):
            value = numToBool(value)
        elif isinstance(value, str):
            value = strToBool(value)

    if not isValidBool(value):
        raise RuntimeError(f'value \"{value}\" for key \"{key}\" is malformed in d: \"{d}\"')

    return value

def getCleanedSplits(s: str | None) -> list[str]:
    if s is not None and not isinstance(s, str):
        raise TypeError(f's argument is malformed: \"{s}\"')

    s = cleanStr(s)
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

def getFloatFromDict(d: dict[str, Any] | None, key: str, fallback: float | None = None) -> float:
    if d is not None and not isinstance(d, dict):
        raise TypeError(f'd argument is malformed: \"{d}\"')
    elif not isValidStr(key):
        raise TypeError(f'key argument is malformed: \"{key}\"')
    elif fallback is not None and not isValidNum(fallback):
        raise TypeError(f'fallback argument is malformed: \"{fallback}\"')

    value: float | None = None

    if d is None or len(d) == 0:
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

def getIntFromDict(d: dict[str, Any] | None, key: str, fallback: int | None = None) -> int:
    if d is not None and not isinstance(d, dict):
        raise TypeError(f'd argument is malformed: \"{d}\"')
    elif not isValidStr(key):
        raise TypeError(f'key argument is malformed: \"{key}\"')
    elif fallback is not None and not isValidNum(fallback):
        raise TypeError(f'fallback argument is malformed: \"{fallback}\"')

    value: float | None = None

    if d is None or len(d) == 0:
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

def getRandomAnimalEmoji() -> str:
    animalEmoji: list[str] = [
        '🐝', '🐛', '🐊', '🐒', '🐓',
        '🐔', '🐕', '🐘', '🐙', '🐚',
        '🐜', '🐞', '🐠', '🐦', '🐧',
        '🐨', '🐩', '🐫', '🐬', '🐭',
        '🐯', '🐰', '🐱', '🐳', '🐴',
        '🐶', '🐷', '🐸', '🐺', '🐻',
        '🐼', '🕊️', '🦁', '🦂', '🦃',
        '🦄', '🦅', '🦆', '🦇', '🦈',
        '🦉', '🦊', '🦋', '🦌', '🦍',
        '🦎', '🦏', '🦒', '🦔', '🦛',
    ]

    return random.choice(animalEmoji)

def getRandomSadEmoji() -> str:
    sadEmoji: list[str] = [ '😭', '😢', '😿', '🤣', '😥', '🥲' ]
    return random.choice(sadEmoji)

def getRandomSpaceEmoji() -> str:
    spaceEmoji: list[str] = [ '🚀', '👾', '☄️', '🌌', '👨‍🚀', '👩‍🚀', '👽', '🌠' ]
    return random.choice(spaceEmoji)

def getShortMaxSafeSize() -> int:
    # taken from Java's Short.MAX_VALUE constant
    return 32767

def getShortMinSafeSize() -> int:
    # taken from Java's Short.MIN_VALUE constant
    return -32768

def getStrFromDict(
    d: dict[str, Any] | frozendict[str, Any] | None,
    key: str,
    fallback: str | None = None,
    clean: bool = False,
    htmlUnescape: bool = False,
    removeCarrots: bool = False
) -> str:
    if not isValidStr(key):
        raise TypeError(f'key argument is malformed: \"{key}\"')
    elif fallback is not None and not isinstance(fallback, str):
        raise TypeError(f'fallback argument is malformed: \"{fallback}\"')
    elif not isValidBool(clean):
        raise TypeError(f'clean argument is malformed: \"{clean}\"')
    elif not isValidBool(htmlUnescape):
        raise TypeError(f'htmlUnescape argument is malformed: \"{htmlUnescape}\"')
    elif not isValidBool(removeCarrots):
        raise TypeError(f'removeCarrots argument is malformed: \"{removeCarrots}\"')

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
        value = cleanStr(
            s = value,
            htmlUnescape = htmlUnescape,
            removeCarrots = removeCarrots,
        )

    return value

T_Sized = TypeVar("T_Sized", bound=Sized)

def hasItems(l: T_Sized | None) -> TypeGuard[T_Sized]:
    return l is not None and len(l) >= 1

def isValidBool(b: bool | Any | None) -> TypeGuard[bool]:
    return b is not None and isinstance(b, bool)

def isValidInt(i: float | Any | None) -> TypeGuard[int]:
    return isValidNum(i) and isinstance(i, int)

def isValidNum(n: float | None) -> TypeGuard[float]:
    return n is not None and isinstance(n, (float, int)) and math.isfinite(n)

def isValidStr(s: str | Any | None) -> TypeGuard[str]:
    """ str len >= 1, not all space """
    return s is not None and isinstance(s, str) and len(s) >= 1 and not s.isspace()

def isValidUrl(s: str | Any | None) -> TypeGuard[str]:
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

def permuteSubArrays(array: list[Any], pos: int = 0) -> Generator[list[Any], None, None]:
    if not isValidInt(pos):
        raise TypeError(f'pos argument is malformed: \"{pos}\"')

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

CHEER_REG_EXES: Final[FrozenList[Pattern]] = FrozenList([
    re.compile(r'(^|\s+)bitboss\d+(\s+|$)', re.IGNORECASE),
    re.compile(r'(^|\s+)cheer\d+(\s+|$)', re.IGNORECASE),
    re.compile(r'(^|\s+)doodlecheer\d+(\s+|$)', re.IGNORECASE),
    re.compile(r'(^|\s+)muxy\d+(\s+|$)', re.IGNORECASE),
    re.compile(r'(^|\s+)streamlabs\d+(\s+|$)', re.IGNORECASE),
    re.compile(r'(^|\s+)uni\d+(\s+|$)', re.IGNORECASE)
])
CHEER_REG_EXES.freeze()

def removeCheerStrings(s: str, repl: str = ' ') -> str:
    if not isinstance(s, str):
        raise TypeError(f's argument is malformed: \"{s}\"')
    elif not isinstance(repl, str):
        raise TypeError(f'repl argument is malformed: \"{repl}\"')

    for cheerRegEx in CHEER_REG_EXES:
        s = cheerRegEx.sub(repl, s.strip()).strip()

    return s.strip()

@overload
def removePreceedingAt(s: None) -> None:
    ...

@overload
def removePreceedingAt(s: str) -> str:
    ...

def removePreceedingAt(s: str | None) -> str | None:
    if s is not None and not isinstance(s, str):
        raise TypeError(f's argument is malformed: \"{s}\"')

    if s is None:
        return None
    elif s.startswith('@'):
        return s[1:]
    else:
        return s

def safeStrToInt(s: str | None) -> int | None:
    if not isValidStr(s):
        return None

    try:
        return int(s)
    except Exception:
        return None

MINUTE_IN_SECONDS: Final[int] = 60
HOUR_IN_SECONDS: Final[int] = 3600
DAY_IN_SECONDS: Final[int] = 86400
WEEK_IN_SECONDS: Final[int] = 604800
YEAR_IN_SECONDS: Final[int] = 31536000

def secondsToDurationMessage(secondsDuration: int) -> str:
    if not isValidInt(secondsDuration):
        raise TypeError(f'secondsDuration argument is malformed: \"{secondsDuration}\"')
    elif secondsDuration < 0 or secondsDuration > getLongMaxSafeSize():
        raise ValueError(f'secondsDuration argument is out of bounds: {secondsDuration}')

    if secondsDuration == 0:
        return '0 seconds'

    years = math.floor(secondsDuration / YEAR_IN_SECONDS)
    if years >= 1: secondsDuration = secondsDuration - (years * YEAR_IN_SECONDS)

    weeks = math.floor(secondsDuration / WEEK_IN_SECONDS)
    if weeks >= 1: secondsDuration = secondsDuration - (weeks * WEEK_IN_SECONDS)

    days = math.floor(secondsDuration / DAY_IN_SECONDS)
    if days >= 1: secondsDuration = secondsDuration - (days * DAY_IN_SECONDS)

    hours = math.floor(secondsDuration / HOUR_IN_SECONDS)
    if hours >= 1: secondsDuration = secondsDuration - (hours * HOUR_IN_SECONDS)

    minutes = math.floor(secondsDuration / MINUTE_IN_SECONDS)
    if minutes >= 1: secondsDuration = secondsDuration - (minutes * MINUTE_IN_SECONDS)

    # the only value now remaining in secondsDuration is the number of seconds
    seconds = secondsDuration

    yearsString = ''
    if years == 1: yearsString = f'{years} year'
    elif years > 1: yearsString = f'{years} years'

    weeksString = ''
    if weeks == 1: weeksString = f'{weeks} week'
    elif weeks > 1: weeksString = f'{weeks} weeks'

    daysString = ''
    if days == 1: daysString = f'{days} day'
    elif days > 1: daysString = f'{days} days'

    hoursString = ''
    if hours == 1: hoursString = f'{hours} hour'
    elif hours > 1: hoursString = f'{hours} hours'

    minutesString = ''
    if minutes == 1: minutesString = f'{minutes} minute'
    elif minutes > 1: minutesString = f'{minutes} minutes'

    secondsString = ''
    if seconds == 1: secondsString = f'{seconds} second'
    elif seconds > 1: secondsString = f'{seconds} seconds'

    result = f'{yearsString} {weeksString} {daysString} {hoursString} {minutesString} {secondsString}'
    return EXTRA_WHITE_SPACE_REG_EX.sub(' ', result).strip()

def splitLongStringIntoMessages(
    maxMessages: int,
    perMessageMaxSize: int,
    message: str | None
) -> list[str]:
    if not isValidInt(maxMessages):
        raise TypeError(f'maxMessages argument is malformed: \"{maxMessages}\"')
    elif maxMessages < 1 or maxMessages >= getIntMaxSafeSize():
        raise ValueError(f'maxMessages argument is out of bounds: {maxMessages}')
    elif not isValidInt(perMessageMaxSize):
        raise TypeError(f'perMessageMaxSize argument is malformed: \"{perMessageMaxSize}\"')
    elif perMessageMaxSize < 50 or perMessageMaxSize >= getIntMaxSafeSize():
        raise ValueError(f'perMessageMaxSize argument is out of bounds: {perMessageMaxSize}')

    messages: list[str] = list()

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

SENTENCES_REG_EX: Final[Pattern] = re.compile(r'(?<=[.!?…])\s+', re.IGNORECASE)

def splitStringIntoSentences(message: str) -> list[str]:
    if not isinstance(message, str):
        raise TypeError(f'message argument is malformed: \"{message}\"')

    sentences: list[str] = list()

    if not isValidStr(message):
        return sentences

    searchResult = SENTENCES_REG_EX.split(message)

    if searchResult is None or len(searchResult) == 0:
        return sentences

    for sentence in searchResult:
        cleanedSentence = cleanStr(sentence)

        if isValidStr(cleanedSentence):
            sentences.append(cleanedSentence)

    return sentences

ALPHANUMERIC_REG_EX: Final[Pattern] = re.compile(r'.*[a-z0-9]+.*', re.IGNORECASE)

def strContainsAlphanumericCharacters(s: str | None) -> TypeGuard[str]:
    if not isValidStr(s):
        return False

    return ALPHANUMERIC_REG_EX.match(s) is not None

TRUE_REG_EX: Final[Pattern] = re.compile(r't(rue)?|y(es)?', re.IGNORECASE)
FALSE_REG_EX: Final[Pattern] = re.compile(r'f(alse)?|n(o)?', re.IGNORECASE)

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

    if TRUE_REG_EX.match(s) is not None:
        return True
    elif FALSE_REG_EX.match(s) is not None:
        return False
    else:
        raise ValueError(f'no matching bool conversion: \"{s}\"')

def strToBool(s: str | None) -> bool:
    """_summary_

    Converts the given string into a bool. None/empty/whitespace strings are converted into True.
    Random strings ("abc123", "asdf", "qwerty", etc) will return True. Only strings that provide a
    match with falseRegEx will return False.

    Parameters
    ------------
    s: str
        The string to convert into a bool (can be None)
    """

    if not isValidStr(s) or FALSE_REG_EX.match(s) is None:
        return True
    else:
        return False
