from abc import ABC, abstractmethod

from .decTalkTtsManagerInterface import DecTalkTtsManagerInterface
from ..ttsManagerProviderInterface import TtsManagerProviderInterface


class DecTalkTtsManagerProviderInterface(TtsManagerProviderInterface, ABC):

    @abstractmethod
    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True
    ) -> DecTalkTtsManagerInterface | None:
        pass

    @abstractmethod
    def getSharedInstance(self) -> DecTalkTtsManagerInterface | None:
        pass
