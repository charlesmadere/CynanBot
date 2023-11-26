from abc import ABC, abstractmethod

from CynanBot.contentScanner.bannedWordType import BannedWordType


class AbsBannedWord(ABC):

    @abstractmethod
    def getType(self) -> BannedWordType:
        pass
