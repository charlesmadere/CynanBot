from abc import ABC, abstractmethod

from .googleTtsManagerInterface import GoogleTtsManagerInterface
from ..models.ttsProvider import TtsProvider
from ..ttsManagerProviderInterface import TtsManagerProviderInterface


class GoogleTtsManagerProviderInterface(TtsManagerProviderInterface, ABC):

    @abstractmethod
    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True
    ) -> GoogleTtsManagerInterface | None:
        pass

    @abstractmethod
    def getSharedInstance(self) -> GoogleTtsManagerInterface | None:
        pass

    @property
    def ttsProvider(self) -> TtsProvider:
        return TtsProvider.GOOGLE
