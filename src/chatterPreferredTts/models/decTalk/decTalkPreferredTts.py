from ..absPreferredTts import AbsPreferredTts
from ..preferredTtsProvider import PreferredTtsProvider


class DecTalkPreferredTts(AbsPreferredTts):

    @property
    def preferredTtsProvider(self) -> PreferredTtsProvider:
        return PreferredTtsProvider.DEC_TALK
