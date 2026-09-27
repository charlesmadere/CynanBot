import random
import re
import uuid
from typing import Final, Pattern

from .randomUtilsInterface import RandomUtilsInterface


class RandomUtils(RandomUtilsInterface):

    def __init__(self):
        self.__uuidRegEx: Final[Pattern] = re.compile(r'[^a-z0-9]', re.IGNORECASE)

    def bool(self) -> bool:
        return bool(random.getrandbits(1))

    def float(self) -> float:
        return random.random()

    def uuid(self) -> str:
        randomUuid = str(uuid.uuid4())
        randomUuid = self.__uuidRegEx.sub('', randomUuid)
        return randomUuid.casefold()
