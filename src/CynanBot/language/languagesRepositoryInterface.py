from abc import ABC, abstractmethod
from typing import Optional

from CynanBot.language.languageEntry import LanguageEntry


class LanguagesRepositoryInterface(ABC):

    @abstractmethod
    async def getAllWotdApiCodes(
        self,
        delimiter: str = ', '
    ) -> str:
        pass

    @abstractmethod
    async def getExampleLanguageEntry(
        self,
        hasIso6391Code: Optional[bool] = None,
        hasWotdApiCode: Optional[bool] = None
    ) -> LanguageEntry:
        pass

    @abstractmethod
    async def getLanguageForCommand(
        self,
        command: str,
        hasIso6391Code: Optional[bool] = None,
        hasWotdApiCode: Optional[bool] = None
    ) -> Optional[LanguageEntry]:
        pass

    @abstractmethod
    async def getLanguageForWotdApiCode(
        self,
        wotdApiCode: str
    ) -> Optional[LanguageEntry]:
        pass

    @abstractmethod
    async def requireLanguageForCommand(
        self,
        command: str,
        hasIso6391Code: Optional[bool] = None,
        hasWotdApiCode: Optional[bool] = None
    ) -> LanguageEntry:
        pass

    @abstractmethod
    async def requireLanguageForWotdApiCode(
        self,
        wotdApiCode: str
    ) -> LanguageEntry:
        pass
