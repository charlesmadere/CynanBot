from abc import abstractmethod

from CynanBot.contentScanner.absBannedWord import AbsBannedWord
from CynanBot.misc.clearable import Clearable


class BannedWordsRepositoryInterface(Clearable):

    @abstractmethod
    def getBannedWords(self) -> set[AbsBannedWord]:
        pass

    @abstractmethod
    async def getBannedWordsAsync(self) -> set[AbsBannedWord]:
        pass
