from dataclasses import dataclass
from typing import Any

from CynanBot.contentScanner.absBannedWord import AbsBannedWord
from CynanBot.contentScanner.bannedWordType import BannedWordType


@dataclass(frozen = True)
class BannedWord(AbsBannedWord):
    word: str

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, BannedWord):
            return self.word.casefold() == other.word.casefold()
        else:
            return False

    def __hash__(self) -> int:
        return hash((self.word.casefold(), self.wordType))

    @property
    def wordType(self) -> BannedWordType:
        return BannedWordType.EXACT_WORD
