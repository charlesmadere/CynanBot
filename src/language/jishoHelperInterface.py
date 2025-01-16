from abc import ABC, abstractmethod

from frozenlist import FrozenList


class JishoHelperInterface(ABC):

    @abstractmethod
    async def search(self, query: str) -> FrozenList[str]:
        pass
