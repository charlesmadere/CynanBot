from dataclasses import dataclass
from typing import Any

from .absBannedWord import AbsBannedWord
from .bannedWordType import BannedWordType


@dataclass(frozen = True, slots = True)
class BannedPhrase(AbsBannedWord):
    phrase: str

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, BannedPhrase):
            return False

        return self.phrase.casefold() == other.phrase.casefold()

    def __hash__(self) -> int:
        return hash((self.phrase.casefold(), self.wordType))

    @property
    def wordType(self) -> BannedWordType:
        return BannedWordType.PHRASE
