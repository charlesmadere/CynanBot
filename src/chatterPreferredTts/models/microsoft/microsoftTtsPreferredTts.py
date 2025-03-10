from ..absPreferredTts import AbsPreferredTts
from ....microsoft.models.microsoftTtsVoice import MicrosoftTtsVoice
from ....tts.models.ttsProvider import TtsProvider


class MicrosoftTtsPreferredTts(AbsPreferredTts):

    def __init__(
        self,
        voice: MicrosoftTtsVoice | None
    ):
        if voice is not None and not isinstance(voice, MicrosoftTtsVoice):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')

        self.__voice: MicrosoftTtsVoice | None = voice

    @property
    def preferredTtsProvider(self) -> TtsProvider:
        return TtsProvider.MICROSOFT

    @property
    def voice(self) -> MicrosoftTtsVoice | None:
        return self.__voice
