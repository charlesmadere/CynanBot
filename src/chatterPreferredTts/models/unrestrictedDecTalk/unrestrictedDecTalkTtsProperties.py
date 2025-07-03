from dataclasses import dataclass

from ..absTtsProperties import AbsTtsProperties
from ....tts.models.ttsProvider import TtsProvider


@dataclass(frozen = True)
class UnrestrictedDecTalkTtsProperties(AbsTtsProperties):

    @property
    def provider(self) -> TtsProvider:
        return TtsProvider.UNRESTRICTED_DEC_TALK
