from ..absPreferredTts import AbsPreferredTts
from ....halfLife.models.halfLifeVoice import HalfLifeVoice
from ....tts.ttsProvider import TtsProvider


class HalfLifePreferredTts(AbsPreferredTts):

    def __init__(
        self,
        halfLifeVoice: HalfLifeVoice
    ):
        if not isinstance(halfLifeVoice, HalfLifeVoice):
            raise TypeError(f'halfLifeVoice argument is malformed: \"{halfLifeVoice}\"')

        self.__halfLifeVoiceEntry: HalfLifeVoice = halfLifeVoice

    @property
    def halfLifeVoiceEntry(self) -> HalfLifeVoice:
        return self.__halfLifeVoiceEntry

    @property
    def preferredTtsProvider(self) -> TtsProvider:
        return TtsProvider.HALF_LIFE
