from typing import Any, Dict

import CynanBot.misc.utils as utils
from CynanBot.contentScanner.absBannedWord import AbsBannedWord
from CynanBot.contentScanner.bannedWordType import BannedWordType


class BannedPhrase(AbsBannedWord):

    def __init__(self, phrase: str):
        if not utils.isValidStr(phrase):
            raise TypeError(f'phrase argument is malformed: \"{phrase}\"')

        self.__phrase: str = phrase.lower()

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, BannedPhrase):
            return self.__phrase == other.__phrase
        else:
            return False

    def getPhrase(self) -> str:
        return self.__phrase

    def getType(self) -> BannedWordType:
        return BannedWordType.PHRASE

    def __hash__(self) -> int:
        return hash((self.__phrase, self.getType()))

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'phrase': self.__phrase,
            'type': self.getType()
        }
