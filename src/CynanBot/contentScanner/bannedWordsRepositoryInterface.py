from abc import abstractmethod
from typing import Set

from contentScanner.absBannedWord import AbsBannedWord
from misc.clearable import Clearable


class BannedWordsRepositoryInterface(Clearable):

    @abstractmethod
    def getBannedWords(self) -> Set[AbsBannedWord]:
        pass

    @abstractmethod
    async def getBannedWordsAsync(self) -> Set[AbsBannedWord]:
        pass
