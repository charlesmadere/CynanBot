from ..language.languageEntry import LanguageEntry


class WotdApiCodeUnavailableException(Exception):

    def __init__(self, languageEntry: LanguageEntry, message: str):
        super().__init__(languageEntry, message)
