from abc import ABC, abstractmethod

from CynanBot.jisho.jishoResponse import JishoResponse


class JishoApiServiceInterface(ABC):

    @abstractmethod
    async def search(self, keyword: str) -> JishoResponse:
        pass
