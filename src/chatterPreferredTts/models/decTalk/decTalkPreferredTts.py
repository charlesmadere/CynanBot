from ..absPreferredTts import AbsPreferredTts
from ....tts.ttsProvider import TtsProvider


class DecTalkPreferredTts(AbsPreferredTts):

    @property
    def preferredTtsProvider(self) -> TtsProvider:
        return TtsProvider.DEC_TALK
