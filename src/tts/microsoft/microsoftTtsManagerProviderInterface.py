from abc import ABC, abstractmethod

from .microsoftTtsManagerInterface import MicrosoftTtsManagerInterface
from ..models.ttsProvider import TtsProvider
from ..ttsManagerProviderInterface import TtsManagerProviderInterface


class MicrosoftTtsManagerProviderInterface(TtsManagerProviderInterface, ABC):

    @abstractmethod
    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True,
    ) -> MicrosoftTtsManagerInterface | None:
        pass

    @abstractmethod
    def getSharedInstance(self) -> MicrosoftTtsManagerInterface | None:
        pass

    @property
    def ttsProvider(self) -> TtsProvider:
        return TtsProvider.MICROSOFT
