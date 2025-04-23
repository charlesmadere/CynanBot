from abc import ABC, abstractmethod

from .decTalkTtsManagerInterface import DecTalkTtsManagerInterface
from ..models.ttsProvider import TtsProvider
from ..ttsManagerProviderInterface import TtsManagerProviderInterface


class DecTalkTtsManagerProviderInterface(TtsManagerProviderInterface, ABC):

    @abstractmethod
    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True
    ) -> DecTalkTtsManagerInterface:
        pass

    @abstractmethod
    def getSharedInstance(self) -> DecTalkTtsManagerInterface:
        pass

    @property
    @abstractmethod
    def ttsProvider(self) -> TtsProvider:
        pass
