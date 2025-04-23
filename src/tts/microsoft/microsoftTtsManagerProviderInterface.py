from abc import ABC, abstractmethod

from .microsoftTtsManagerInterface import MicrosoftTtsManagerInterface
from ..models.ttsProvider import TtsProvider
from ..ttsManagerProviderInterface import TtsManagerProviderInterface


class MicrosoftTtsManagerProviderInterface(TtsManagerProviderInterface, ABC):

    @abstractmethod
    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True
    ) -> MicrosoftTtsManagerInterface:
        pass

    @abstractmethod
    def getSharedInstance(self) -> MicrosoftTtsManagerInterface:
        pass

    @property
    @abstractmethod
    def ttsProvider(self) -> TtsProvider:
        pass
