from ..absTtsProperties import AbsTtsProperties
from ....tts.models.ttsProvider import TtsProvider


class CommodoreSamTtsProperties(AbsTtsProperties):

    @property
    def provider(self) -> TtsProvider:
        return TtsProvider.COMMODORE_SAM
