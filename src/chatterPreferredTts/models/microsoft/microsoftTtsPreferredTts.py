from typing import Final

from ..absTtsProperties import AbsTtsProperties
from ....microsoft.models.microsoftTtsVoice import MicrosoftTtsVoice
from ....tts.models.ttsProvider import TtsProvider


class MicrosoftTtsTtsProperties(AbsTtsProperties):

    def __init__(
        self,
        voice: MicrosoftTtsVoice | None
    ):
        if voice is not None and not isinstance(voice, MicrosoftTtsVoice):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')

        self.__voice: Final[MicrosoftTtsVoice | None] = voice

    @property
    def provider(self) -> TtsProvider:
        return TtsProvider.MICROSOFT

    @property
    def voice(self) -> MicrosoftTtsVoice | None:
        return self.__voice
