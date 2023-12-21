from abc import ABC, abstractmethod
from typing import Optional, Set

from CynanBot.contentScanner.contentCode import ContentCode


class ContentScannerInterface(ABC):

    @abstractmethod
    async def scan(self, message: Optional[str]) -> ContentCode:
        pass

    @abstractmethod
    async def updatePhrasesContent(
        self,
        phrases: Set[Optional[str]],
        string: Optional[str]
    ):
        pass

    @abstractmethod
    async def updateWordsContent(
        self,
        words: Set[Optional[str]],
        string: Optional[str]
    ):
        pass
