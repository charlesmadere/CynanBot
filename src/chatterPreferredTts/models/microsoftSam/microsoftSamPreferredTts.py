from typing import Final

from ..absTtsProperties import AbsTtsProperties
from ....microsoftSam.models.microsoftSamVoice import MicrosoftSamVoice
from ....tts.models.ttsProvider import TtsProvider


class MicrosoftSamTtsProperties(AbsTtsProperties):

    def __init__(
        self,
        voice: MicrosoftSamVoice | None
    ):
        if voice is not None and not isinstance(voice, MicrosoftSamVoice):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')

        self.__voice: Final[MicrosoftSamVoice | None] = voice

    @property
    def provider(self) -> TtsProvider:
        return TtsProvider.MICROSOFT_SAM

    @property
    def voice(self) -> MicrosoftSamVoice | None:
        return self.__voice
