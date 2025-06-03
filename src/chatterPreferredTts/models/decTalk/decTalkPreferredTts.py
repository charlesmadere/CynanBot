from typing import Final

from ..absTtsProperties import AbsTtsProperties
from ....decTalk.models.decTalkVoice import DecTalkVoice
from ....tts.models.ttsProvider import TtsProvider


class DecTalkTtsProperties(AbsTtsProperties):

    def __init__(
        self,
        voice: DecTalkVoice | None
    ):
        if voice is not None and not isinstance(voice, DecTalkVoice):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')

        self.__voice: Final[DecTalkVoice | None] = voice

    @property
    def provider(self) -> TtsProvider:
        return TtsProvider.DEC_TALK

    @property
    def voice(self) -> DecTalkVoice | None:
        return self.__voice
