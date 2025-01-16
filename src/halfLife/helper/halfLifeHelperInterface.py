from abc import ABC, abstractmethod

from frozenlist import FrozenList


class HalfLifeHelperInterface(ABC):

    @abstractmethod
    async def getSpeech(
        self,
        message: str | None
    ) -> FrozenList[str] | None:
        pass
