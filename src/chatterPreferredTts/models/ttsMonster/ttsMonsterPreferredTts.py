from ..absPreferredTts import AbsPreferredTts
from ....tts.models.ttsProvider import TtsProvider
from ....ttsMonster.models.ttsMonsterVoice import TtsMonsterVoice


class TtsMonsterPreferredTts(AbsPreferredTts):

    def __init__(
        self,
        voice: TtsMonsterVoice | None
    ):
        if voice is not None and not isinstance(voice, TtsMonsterVoice):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')

        self.__voice: TtsMonsterVoice | None = voice

    @property
    def preferredTtsProvider(self) -> TtsProvider:
        return TtsProvider.TTS_MONSTER

    @property
    def voice(self) -> TtsMonsterVoice | None:
        return self.__voice
