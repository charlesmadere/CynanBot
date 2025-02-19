from ..absPreferredTts import AbsPreferredTts
from ..preferredTtsProvider import PreferredTtsProvider


class MicrosoftSamPreferredTts(AbsPreferredTts):

    @property
    def preferredTtsProvider(self) -> PreferredTtsProvider:
        return PreferredTtsProvider.MICROSOFT_SAM
