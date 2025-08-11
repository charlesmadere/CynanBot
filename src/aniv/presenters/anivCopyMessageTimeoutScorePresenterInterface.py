from abc import ABC, abstractmethod

from ..models.preparedAnivCopyMessageTimeoutScore import PreparedAnivCopyMessageTimeoutScore
from ...language.languageEntry import LanguageEntry


class AnivCopyMessageTimeoutScorePresenterInterface(ABC):

    @abstractmethod
    async def getChannelEditorsCantPlayString(
        self,
        language: LanguageEntry,
    ) -> str:
        pass

    @abstractmethod
    async def getScoreString(
        self,
        language: LanguageEntry,
        preparedScore: PreparedAnivCopyMessageTimeoutScore,
    ) -> str:
        pass
