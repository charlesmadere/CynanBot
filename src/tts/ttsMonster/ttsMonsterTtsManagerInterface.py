from abc import ABC

from ..models.ttsProvider import TtsProvider
from ..ttsManagerInterface import TtsManagerInterface


class TtsMonsterTtsManagerInterface(TtsManagerInterface, ABC):

    @property
    def ttsProvider(self) -> TtsProvider:
        return TtsProvider.TTS_MONSTER
