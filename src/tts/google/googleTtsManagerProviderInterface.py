from abc import ABC, abstractmethod

from .googleTtsManagerInterface import GoogleTtsManagerInterface
from ..models.ttsProvider import TtsProvider
from ..ttsManagerProviderInterface import TtsManagerProviderInterface


class GoogleTtsManagerProviderInterface(TtsManagerProviderInterface, ABC):

    @abstractmethod
    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True
    ) -> GoogleTtsManagerInterface:
        pass

    @abstractmethod
    def getSharedInstance(self) -> GoogleTtsManagerInterface:
        pass

    @property
    @abstractmethod
    def ttsProvider(self) -> TtsProvider:
        pass
