from dataclasses import dataclass
from typing import Any

from .absBannedWord import AbsBannedWord
from .bannedWordType import BannedWordType


@dataclass(frozen = True)
class BannedPhrase(AbsBannedWord):
    phrase: str

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, BannedPhrase):
            return self.phrase.casefold() == other.phrase.casefold()
        else:
            return False

    def __hash__(self) -> int:
        return hash((self.phrase.casefold(), self.wordType))

    @property
    def wordType(self) -> BannedWordType:
        return BannedWordType.PHRASE
