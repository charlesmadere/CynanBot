import random
import re
import uuid
from typing import Any, Final, MutableSequence, Sequence, Pattern, TypeVar

from .randomUtilsInterface import RandomUtilsInterface

T = TypeVar('T')


class RandomUtils(RandomUtilsInterface):

    def __init__(self):
        self.__uuidRegEx: Final[Pattern] = re.compile(r'[^a-z0-9]', re.IGNORECASE)

    def bool(self) -> bool:
        return bool(random.getrandbits(1))

    def choice(self, collection: Sequence[T]) -> T:
        if not isinstance(collection, Sequence):
            raise TypeError(f'collection argument is malformed: \"{collection}\"')
        if len(collection) == 0:
            raise IndexError("Cannot choose from an empty sequence")

        return random.choice(collection)

    def float(self) -> float:
        return random.random()

    def int(self, low: int, high: int) -> int:
        if not isinstance(low, int):
            raise TypeError(f'low argument is malformed: \"{low}\"')
        elif not isinstance(high, int):
            raise TypeError(f'high argument is malformed: \"{high}\"')
        elif high < low:
            raise ValueError(f'high argument can\'t be less than low ({high=}) ({low=})')

        return random.randint(low, high)

    def shuffle(self, collection: MutableSequence[Any]):
        if not isinstance(collection, MutableSequence):
            raise TypeError(f'collection argument is malformed: \"{collection}\"')

        random.shuffle(collection)

    def uuid(self) -> str:
        randomUuid = str(uuid.uuid4())
        randomUuid = self.__uuidRegEx.sub('', randomUuid)
        return randomUuid.casefold()
