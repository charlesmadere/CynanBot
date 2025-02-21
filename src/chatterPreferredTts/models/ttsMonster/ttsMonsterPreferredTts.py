from ..absPreferredTts import AbsPreferredTts
from ....tts.ttsProvider import TtsProvider


class TtsMonsterPreferredTts(AbsPreferredTts):

    @property
    def preferredTtsProvider(self) -> TtsProvider:
        return TtsProvider.TTS_MONSTER
