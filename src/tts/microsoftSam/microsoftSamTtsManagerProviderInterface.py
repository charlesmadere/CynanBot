from abc import ABC, abstractmethod

from .microsoftSamTtsManagerInterface import MicrosoftSamTtsManagerInterface
from ..models.ttsProvider import TtsProvider
from ..ttsManagerProviderInterface import TtsManagerProviderInterface


class MicrosoftSamTtsManagerProviderInterface(TtsManagerProviderInterface, ABC):

    @abstractmethod
    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True
    ) -> MicrosoftSamTtsManagerInterface | None:
        pass

    @abstractmethod
    def getSharedInstance(self) -> MicrosoftSamTtsManagerInterface | None:
        pass

    @property
    def ttsProvider(self) -> TtsProvider:
        return TtsProvider.MICROSOFT_SAM
