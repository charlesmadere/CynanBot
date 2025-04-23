from abc import ABC, abstractmethod

from .microsoftSamTtsManagerInterface import MicrosoftSamTtsManagerInterface
from ..models.ttsProvider import TtsProvider
from ..ttsManagerProviderInterface import TtsManagerProviderInterface


class MicrosoftSamTtsManagerProviderInterface(TtsManagerProviderInterface, ABC):

    @abstractmethod
    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True
    ) -> MicrosoftSamTtsManagerInterface:
        pass

    @abstractmethod
    def getSharedInstance(self) -> MicrosoftSamTtsManagerInterface:
        pass

    @property
    @abstractmethod
    def ttsProvider(self) -> TtsProvider:
        pass
