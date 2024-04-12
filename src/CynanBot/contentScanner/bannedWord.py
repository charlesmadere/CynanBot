from typing import Any

import CynanBot.misc.utils as utils
from CynanBot.contentScanner.absBannedWord import AbsBannedWord
from CynanBot.contentScanner.bannedWordType import BannedWordType


class BannedWord(AbsBannedWord):

    def __init__(self, word: str):
        if not utils.isValidStr(word):
            raise TypeError(f'word argument is malformed: \"{word}\"')

        self.__word: str = word.lower()

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, BannedWord):
            return self.__word == other.__word
        else:
            return False

    def getType(self) -> BannedWordType:
        return BannedWordType.EXACT_WORD

    def getWord(self) -> str:
        return self.__word

    def __hash__(self) -> int:
        return hash((self.__word, self.getType()))

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'type': self.getType(),
            'word': self.__word
        }
