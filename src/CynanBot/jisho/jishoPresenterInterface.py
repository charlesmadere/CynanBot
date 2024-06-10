from abc import ABC, abstractmethod

from CynanBot.jisho.jishoResponse import JishoResponse


class JishoPresenterInterface(ABC):

    @abstractmethod
    async def toStrings(self, jishoResponse: JishoResponse) -> list[str]:
        pass
