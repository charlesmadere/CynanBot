from abc import ABC, abstractmethod

from CynanBot.aniv.anivCopyMessageTimeoutScore import \
    AnivCopyMessageTimeoutScore


class AnivCopyMessageTimeoutScorePresenterInterface(ABC):

    @abstractmethod
    async def toString(self, score: AnivCopyMessageTimeoutScore) -> str:
        pass
