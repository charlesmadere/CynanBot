from typing import Any

import misc.utils as utils
from contentScanner.absBannedWord import AbsBannedWord
from contentScanner.bannedWordType import BannedWordType


class BannedWord(AbsBannedWord):

    def __init__(self, word: str):
        if not utils.isValidStr(word):
            raise ValueError(f'word argument is malformed: \"{word}\"')

        self.__word: str = word.lower()

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, AbsBannedWord):
            if isinstance(other, BannedWord):
                return self.__word == other.__word
            else:
                return False
        else:
            return False

    def getType(self) -> BannedWordType:
        return BannedWordType.EXACT_WORD

    def getWord(self) -> str:
        return self.__word

    def __hash__(self) -> int:
        return hash((self.__word, self.getType()))

    def __str__(self) -> str:
        return f'word=\"{self.__word}\", type=\"{self.getType()}\"'
