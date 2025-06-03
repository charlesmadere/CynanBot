from typing import Final

from ..absTtsProperties import AbsTtsProperties
from ....halfLife.models.halfLifeVoice import HalfLifeVoice
from ....tts.models.ttsProvider import TtsProvider


class HalfLifeTtsProperties(AbsTtsProperties):

    def __init__(
        self,
        voice: HalfLifeVoice | None
    ):
        if voice is not None and not isinstance(voice, HalfLifeVoice):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')

        self.__voice: Final[HalfLifeVoice | None] = voice

    @property
    def provider(self) -> TtsProvider:
        return TtsProvider.HALF_LIFE

    @property
    def voice(self) -> HalfLifeVoice | None:
        return self.__voice
