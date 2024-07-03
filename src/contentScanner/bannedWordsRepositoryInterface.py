from abc import abstractmethod

from .absBannedWord import AbsBannedWord
from ..misc.clearable import Clearable


class BannedWordsRepositoryInterface(Clearable):

    @abstractmethod
    def getBannedWords(self) -> set[AbsBannedWord]:
        pass

    @abstractmethod
    async def getBannedWordsAsync(self) -> set[AbsBannedWord]:
        pass
