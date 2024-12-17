from abc import ABC, abstractmethod

from .anivCopyMessageTimeoutScore import AnivCopyMessageTimeoutScore
from ..language.languageEntry import LanguageEntry


class AnivCopyMessageTimeoutScorePresenterInterface(ABC):

    @abstractmethod
    async def toString(
        self,
        score: AnivCopyMessageTimeoutScore,
        language: LanguageEntry
    ) -> str:
        pass
