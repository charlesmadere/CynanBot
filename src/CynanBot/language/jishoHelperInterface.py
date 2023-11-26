from abc import ABC, abstractmethod

from CynanBot.language.jishoResult import JishoResult


class JishoHelperInterface(ABC):

    @abstractmethod
    async def search(self, query: str) -> JishoResult:
        pass
