from abc import ABC, abstractmethod

from CynanBot.contentScanner.bannedWordType import BannedWordType


class AbsBannedWord(ABC):

    @property
    @abstractmethod
    def wordType(self) -> BannedWordType:
        pass
