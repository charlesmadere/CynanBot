from ..absPreferredTts import AbsPreferredTts
from ....tts.ttsProvider import TtsProvider


class SingingDecTalkPreferredTts(AbsPreferredTts):

    @property
    def preferredTtsProvider(self) -> TtsProvider:
        return TtsProvider.SINGING_DEC_TALK
