from abc import ABC, abstractmethod

from frozenlist import FrozenList


class TempFileHelperInterface(ABC):

    @abstractmethod
    async def getTempFileName(
        self,
        prefix: str,
        extension: str
    ) -> str:
        pass

    @abstractmethod
    async def getTempFileNames(
        self,
        amount: int,
        prefix: str,
        extension: str
    ) -> FrozenList[str]:
        pass
