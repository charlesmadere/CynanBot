from abc import ABC, abstractmethod

from .jishoResponse import JishoResponse


class JishoPresenterInterface(ABC):

    @abstractmethod
    async def toStrings(
        self,
        includeRomaji: bool,
        jishoResponse: JishoResponse
    ) -> list[str]:
        pass
