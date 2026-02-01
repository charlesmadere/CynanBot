from .languageEntry import LanguageEntry
from .translationApiSource import TranslationApiSource
from ..contentScanner.contentCode import ContentCode
from ..transparent.transparentResponse import TransparentResponse


class NoLanguageEntryFoundForCommandException(Exception):

    def __init__(self, message: str, command: str):
        if not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not isinstance(command, str):
            raise TypeError(f'command argument is malformed: \"{command}\"')

        super().__init__(message, command)


class NoLanguageEntryFoundForWotdApiCodeException(Exception):

    def __init__(self, message: str, wotdApiCode: str):
        if not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not isinstance(wotdApiCode, str):
            raise TypeError(f'wotdApiCode argument is malformed: \"{wotdApiCode}\"')

        super().__init__(message, wotdApiCode)


class NoTranslationEnginesAvailableException(Exception):

    def __init__(self, message: str):
        if not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')

        super().__init__(message)


class TranslationEngineUnavailableException(Exception):

    def __init__(
        self,
        message: str,
        translationApiSource: TranslationApiSource
    ):
        if not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not isinstance(translationApiSource, TranslationApiSource):
            raise TypeError(f'translationApiSource argument is malformed: \"{translationApiSource}\"')

        super().__init__(message, translationApiSource)


class TranslationLanguageHasNoIso6391Code(Exception):

    def __init__(
        self,
        languageEntry: LanguageEntry,
        message: str
    ):
        if not isinstance(languageEntry, LanguageEntry):
            raise TypeError(f'languageEntry argument is malformed: \"{languageEntry}\"')
        elif not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')

        super().__init__(languageEntry, message)


class TranslationException(Exception):

    def __init__(
        self,
        message: str,
        translationApiSource: TranslationApiSource
    ):
        if not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not isinstance(translationApiSource, TranslationApiSource):
            raise TypeError(f'translationApiSource argument is malformed: \"{translationApiSource}\"')

        super().__init__(message, translationApiSource)


class WordOfTheDayHasBadContentException(Exception):

    def __init__(
        self,
        contentCodes: frozenset[ContentCode],
        languageEntry: LanguageEntry,
        transparentResponse: TransparentResponse,
    ):
        if not isinstance(contentCodes, frozenset):
            raise TypeError(f'contentCodes argument is malformed: \"{contentCodes}\"')
        elif not isinstance(languageEntry, LanguageEntry):
            raise TypeError(f'languageEntry argument is malformed: \"{languageEntry}\"')
        elif not isinstance(transparentResponse, TransparentResponse):
            raise TypeError(f'transparentResponse argument is malformed: \"{transparentResponse}\"')

        super().__init__(contentCodes, languageEntry, transparentResponse)
