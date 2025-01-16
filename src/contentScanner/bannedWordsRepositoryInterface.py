from abc import abstractmethod

from .absBannedWord import AbsBannedWord
from ..misc.clearable import Clearable


class BannedWordsRepositoryInterface(Clearable):

    @abstractmethod
    def getBannedWords(self) -> frozenset[AbsBannedWord]:
        pass

    @abstractmethod
    async def getBannedWordsAsync(self) -> frozenset[AbsBannedWord]:
        pass
