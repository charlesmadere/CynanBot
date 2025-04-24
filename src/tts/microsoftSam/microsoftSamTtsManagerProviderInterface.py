from abc import ABC, abstractmethod

from .microsoftSamTtsManagerInterface import MicrosoftSamTtsManagerInterface
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
