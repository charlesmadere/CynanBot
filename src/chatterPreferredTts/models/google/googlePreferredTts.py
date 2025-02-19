from ..absPreferredTts import AbsPreferredTts
from ..preferredTtsProvider import PreferredTtsProvider
from ....language.languageEntry import LanguageEntry


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
    def preferredTtsProvider(self) -> PreferredTtsProvider:
        return PreferredTtsProvider.GOOGLE
