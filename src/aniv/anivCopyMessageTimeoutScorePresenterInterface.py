from abc import ABC, abstractmethod

from .anivCopyMessageTimeoutScore import AnivCopyMessageTimeoutScore


class AnivCopyMessageTimeoutScorePresenterInterface(ABC):

    @abstractmethod
    async def toString(self, score: AnivCopyMessageTimeoutScore) -> str:
        pass
