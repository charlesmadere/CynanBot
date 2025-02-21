from ..absPreferredTts import AbsPreferredTts
from ....language.languageEntry import LanguageEntry
from ....tts.ttsProvider import TtsProvider


class GooglePreferredTts(AbsPreferredTts):

    def __init__(
        self,
        languageEntry: LanguageEntry | None
    ):
        if languageEntry is not None and not isinstance(languageEntry, LanguageEntry):
            raise TypeError(f'languageEntry argument is malformed: \"{languageEntry}\"')

        self.__languageEntry: LanguageEntry | None = languageEntry

    @property
    def languageEntry(self) -> LanguageEntry | None:
        return self.__languageEntry

    @property
    def preferredTtsProvider(self) -> TtsProvider:
        return TtsProvider.GOOGLE
