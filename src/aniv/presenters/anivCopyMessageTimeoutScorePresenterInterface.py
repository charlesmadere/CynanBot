from abc import ABC, abstractmethod

from ..models.anivCopyMessageTimeoutScore import AnivCopyMessageTimeoutScore
from ...language.languageEntry import LanguageEntry


class AnivCopyMessageTimeoutScorePresenterInterface(ABC):

    @abstractmethod
    async def getChannelEditorsCantPlayString(
        self,
        language: LanguageEntry,
    ) -> str:
        pass

    @abstractmethod
    async def toString(
        self,
        score: AnivCopyMessageTimeoutScore | None,
        language: LanguageEntry,
        chatterUserName: str,
    ) -> str:
        pass
