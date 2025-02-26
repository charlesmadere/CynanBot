from ..absPreferredTts import AbsPreferredTts
from ....microsoftSam.models.microsoftSamVoice import MicrosoftSamVoice
from ....tts.models.ttsProvider import TtsProvider


class MicrosoftSamPreferredTts(AbsPreferredTts):

    def __init__(
        self,
        microsoftSamVoice: MicrosoftSamVoice | None
    ):
        if microsoftSamVoice is not None and not isinstance(microsoftSamVoice, MicrosoftSamVoice):
            raise TypeError(f'microsoftSamVoice argument is malformed: \"{microsoftSamVoice}\"')

        self.__microsoftSamVoiceEntry: MicrosoftSamVoice | None = microsoftSamVoice

    @property
    def microsoftSamVoiceEntry(self) -> MicrosoftSamVoice | None:
        return self.__microsoftSamVoiceEntry

    @property
    def preferredTtsProvider(self) -> TtsProvider:
        return TtsProvider.MICROSOFT_SAM
