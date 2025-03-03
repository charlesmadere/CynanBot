from ..absPreferredTts import AbsPreferredTts
from ....decTalk.models.decTalkVoice import DecTalkVoice
from ....tts.models.ttsProvider import TtsProvider


class DecTalkPreferredTts(AbsPreferredTts):

    def __init__(
        self,
        voice: DecTalkVoice | None
    ):
        if voice is not None and not isinstance(voice, DecTalkVoice):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')

        self.__voice: DecTalkVoice | None = voice

    @property
    def preferredTtsProvider(self) -> TtsProvider:
        return TtsProvider.DEC_TALK

    @property
    def voice(self) -> DecTalkVoice | None:
        return self.__voice
