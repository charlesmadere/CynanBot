from abc import ABC, abstractmethod

from CynanBot.contentScanner.contentCode import ContentCode


class ContentScannerInterface(ABC):

    @abstractmethod
    async def scan(self, message: str | None) -> ContentCode:
        pass

    @abstractmethod
    async def updatePhrasesContent(
        self,
        phrases: set[str],
        string: str | None
    ):
        pass

    @abstractmethod
    async def updateWordsContent(
        self,
        words: set[str],
        string: str | None
    ):
        pass
