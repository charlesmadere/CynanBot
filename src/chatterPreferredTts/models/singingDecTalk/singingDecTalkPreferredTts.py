from ..absTtsProperties import AbsTtsProperties
from ....tts.models.ttsProvider import TtsProvider


class SingingDecTalkTtsProperties(AbsTtsProperties):

    @property
    def provider(self) -> TtsProvider:
        return TtsProvider.SINGING_DEC_TALK
