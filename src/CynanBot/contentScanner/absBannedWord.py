from abc import ABC, abstractmethod

from contentScanner.bannedWordType import BannedWordType


class AbsBannedWord(ABC):

    @abstractmethod
    def getType(self) -> BannedWordType:
        pass
