from abc import ABC, abstractmethod

from .decTalkTtsManagerInterface import DecTalkTtsManagerInterface
from ..models.ttsProvider import TtsProvider
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

    @property
    def ttsProvider(self) -> TtsProvider:
        return TtsProvider.DEC_TALK
