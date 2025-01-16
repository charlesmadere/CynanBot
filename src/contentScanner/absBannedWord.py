from abc import ABC, abstractmethod

from .bannedWordType import BannedWordType


class AbsBannedWord(ABC):

    @property
    @abstractmethod
    def wordType(self) -> BannedWordType:
        pass
