from ..absPreferredTts import AbsPreferredTts
from ....tts.models.ttsProvider import TtsProvider
from ....ttsMonster.models.ttsMonsterVoice import TtsMonsterVoice

class TtsMonsterPreferredTts(AbsPreferredTts):

    def __init__(
        self,
        ttsMonsterVoice: TtsMonsterVoice | None
    ):
        if ttsMonsterVoice is not None and not isinstance(ttsMonsterVoice, TtsMonsterVoice):
            raise TypeError(f'ttsMonsterVoiceEntry argument is malformed: \"{ttsMonsterVoice}\"')

        self.__ttsMonsterVoiceEntry: TtsMonsterVoice | None = ttsMonsterVoice

    @property
    def ttsMonsterVoiceEntry(self) -> TtsMonsterVoice | None:
        return self.__ttsMonsterVoiceEntry

    @property
    def preferredTtsProvider(self) -> TtsProvider:
        return TtsProvider.TTS_MONSTER
