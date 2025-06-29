from abc import ABC

from ..models.ttsProvider import TtsProvider
from ..ttsManagerInterface import TtsManagerInterface


class MicrosoftTtsManagerInterface(TtsManagerInterface, ABC):

    @property
    def ttsProvider(self) -> TtsProvider:
        return TtsProvider.MICROSOFT
