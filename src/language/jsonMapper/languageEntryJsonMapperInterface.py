from abc import ABC, abstractmethod
from typing import Any

from ..languageEntry import LanguageEntry


class LanguageEntryJsonMapperInterface(ABC):

    @abstractmethod
    def parseLanguageEntry(
        self,
        jsonString: str | Any | None
    ) -> LanguageEntry | None:
        pass

    @abstractmethod
    def requireLanguageEntry(
        self,
        jsonString: str | Any | None
    ) -> LanguageEntry:
        pass

    @abstractmethod
    def serializeLanguageEntry(
        self,
        languageEntry: LanguageEntry
    ) -> str:
        pass
