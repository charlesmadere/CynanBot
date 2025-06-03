from typing import Final

from ..absTtsProperties import AbsTtsProperties
from ....language.languageEntry import LanguageEntry
from ....tts.models.ttsProvider import TtsProvider


class GoogleTtsProperties(AbsTtsProperties):

    def __init__(
        self,
        languageEntry: LanguageEntry | None
    ):
        if languageEntry is not None and not isinstance(languageEntry, LanguageEntry):
            raise TypeError(f'languageEntry argument is malformed: \"{languageEntry}\"')

        self.__languageEntry: Final[LanguageEntry | None] = languageEntry

    @property
    def languageEntry(self) -> LanguageEntry | None:
        return self.__languageEntry

    @property
    def provider(self) -> TtsProvider:
        return TtsProvider.GOOGLE
