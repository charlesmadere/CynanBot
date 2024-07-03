from abc import ABC, abstractmethod

from .jishoResponse import JishoResponse


class JishoApiServiceInterface(ABC):

    @abstractmethod
    async def search(self, keyword: str) -> JishoResponse:
        pass
