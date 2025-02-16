from abc import ABC, abstractmethod

from ..ttsProvider import TtsProvider


class TtsDirectoryProviderInterface(ABC):

    @abstractmethod
    async def getFullTtsDirectoryFor(self, provider: TtsProvider) -> str:
        pass

    @abstractmethod
    async def getRootTtsDirectory(self) -> str:
        pass

    @abstractmethod
    async def getTtsDirectoryFor(self, provider: TtsProvider) -> str:
        pass
