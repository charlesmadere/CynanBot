from ..absPreferredTts import AbsPreferredTts
from ....tts.ttsProvider import TtsProvider

from src.misc import utils

class TtsMonsterPreferredTts(AbsPreferredTts):

    def __init__(
        self,
        ttsMonsterVoice: str | None
    ):
        self.__ttsMonsterVoiceEntry: str | None = None

        if utils.isValidStr(ttsMonsterVoice):
            self.__ttsMonsterVoiceEntry = f'{ttsMonsterVoice}: '

    @property
    def ttsMonsterVoiceEntry(self) -> str | None:
        return self.__ttsMonsterVoiceEntry

    @property
    def preferredTtsProvider(self) -> TtsProvider:
        return TtsProvider.TTS_MONSTER
