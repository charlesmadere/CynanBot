from typing import Final

from ..absTtsProperties import AbsTtsProperties
from ....tts.models.ttsProvider import TtsProvider
from ....ttsMonster.models.ttsMonsterVoice import TtsMonsterVoice


class TtsMonsterTtsProperties(AbsTtsProperties):

    def __init__(
        self,
        voice: TtsMonsterVoice | None
    ):
        if voice is not None and not isinstance(voice, TtsMonsterVoice):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')

        self.__voice: Final[TtsMonsterVoice | None] = voice

    @property
    def provider(self) -> TtsProvider:
        return TtsProvider.TTS_MONSTER

    @property
    def voice(self) -> TtsMonsterVoice | None:
        return self.__voice
