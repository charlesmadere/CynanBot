from abc import ABC, abstractmethod

from frozenlist import FrozenList

from .jishoResponse import JishoResponse


class JishoPresenterInterface(ABC):

    @abstractmethod
    async def toStrings(
        self,
        includeRomaji: bool,
        jishoResponse: JishoResponse,
    ) -> FrozenList[str]:
        pass
