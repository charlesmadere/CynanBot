from abc import ABC, abstractmethod

from .languageEntry import LanguageEntry


class LanguagesRepositoryInterface(ABC):

    @abstractmethod
    async def getAllWotdApiCodes(
        self,
        delimiter: str = ', ',
    ) -> str:
        pass

    @abstractmethod
    async def getExampleLanguageEntry(
        self,
        hasIso6391Code: bool | None = None,
        hasWotdApiCode: bool | None = None,
    ) -> LanguageEntry:
        pass

    @abstractmethod
    async def getLanguageForCommand(
        self,
        command: str,
        hasIso6391Code: bool | None = None,
        hasWotdApiCode: bool | None = None,
    ) -> LanguageEntry | None:
        pass

    @abstractmethod
    async def getLanguageForIso6391Code(
        self,
        iso6391Code: str,
    ) -> LanguageEntry | None:
        pass

    @abstractmethod
    async def getLanguageForWotdApiCode(
        self,
        wotdApiCode: str,
    ) -> LanguageEntry | None:
        pass

    @abstractmethod
    async def requireLanguageForCommand(
        self,
        command: str,
        hasIso6391Code: bool | None = None,
        hasWotdApiCode: bool | None = None,
    ) -> LanguageEntry:
        pass

    @abstractmethod
    async def requireLanguageForWotdApiCode(
        self,
        wotdApiCode: str,
    ) -> LanguageEntry:
        pass
