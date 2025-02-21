from abc import ABC, abstractmethod

from .absBannedWord import AbsBannedWord
from ..misc.clearable import Clearable


class BannedWordsRepositoryInterface(Clearable, ABC):

    @abstractmethod
    def getBannedWords(self) -> frozenset[AbsBannedWord]:
        pass

    @abstractmethod
    async def getBannedWordsAsync(self) -> frozenset[AbsBannedWord]:
        pass
