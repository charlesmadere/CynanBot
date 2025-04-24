from abc import ABC, abstractmethod

from .halfLifeTtsManagerInterface import HalfLifeTtsManagerInterface
from ..ttsManagerProviderInterface import TtsManagerProviderInterface


class HalfLifeTtsManagerProviderInterface(TtsManagerProviderInterface, ABC):

    @abstractmethod
    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True
    ) -> HalfLifeTtsManagerInterface | None:
        pass

    @abstractmethod
    def getSharedInstance(self) -> HalfLifeTtsManagerInterface | None:
        pass
