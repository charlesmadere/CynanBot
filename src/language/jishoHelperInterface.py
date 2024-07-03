from abc import ABC, abstractmethod


class JishoHelperInterface(ABC):

    @abstractmethod
    async def search(self, query: str) -> list[str]:
        pass
