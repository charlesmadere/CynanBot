from .languageEntry import LanguageEntry
from .translationApiSource import TranslationApiSource
from ..misc import utils as utils


class TranslationResponse:

    def __init__(
        self,
        originalLanguage: LanguageEntry | None,
        translatedLanguage: LanguageEntry | None,
        originalText: str,
        translatedText: str,
        translationApiSource: TranslationApiSource,
    ):
        if originalLanguage is not None and not utils.isValidStr(originalLanguage.iso6391Code):
            raise ValueError(f'originalLanguage argument must be either None or have an ISO 639-1 code: \"{originalLanguage}\"')
        elif translatedLanguage is not None and not utils.isValidStr(translatedLanguage.iso6391Code):
            raise ValueError(f'translatedLanguage argument must be either None or have an ISO 639-1 code: \"{translatedLanguage}\"')
        elif not utils.isValidStr(originalText):
            raise ValueError(f'originalText argument is malformed: \"{originalText}\"')
        elif not utils.isValidStr(translatedText):
            raise ValueError(f'translatedText argument is malformed: \"{translatedText}\"')
        elif not isinstance(translationApiSource, TranslationApiSource):
            raise ValueError(f'translationApiSource argument is malformed: \"{translationApiSource}\"')

        self.__originalLanguage: LanguageEntry | None = originalLanguage
        self.__translatedLanguage: LanguageEntry | None = translatedLanguage
        self.__originalText: str = originalText
        self.__translatedText: str = translatedText
        self.__translationApiSource: TranslationApiSource = translationApiSource

    def getOriginalLanguage(self) -> LanguageEntry | None:
        return self.__originalLanguage

    def getOriginalText(self) -> str:
        return self.__originalText

    def getTranslatedLanguage(self) -> LanguageEntry | None:
        return self.__translatedLanguage

    def getTranslatedText(self) -> str:
        return self.__translatedText

    def toStr(self) -> str:
        prefixText = ''
        originalLanguage = self.__originalLanguage
        translatedLanguage = self.__translatedLanguage

        if originalLanguage is not None:
            if translatedLanguage is not None:
                firstLangText = ''
                if utils.isValidStr(originalLanguage.flag):
                    firstLangText = originalLanguage.flag
                else:
                    firstLangText = originalLanguage.requireIso6391Code().upper()

                secondLangText = ''
                if utils.isValidStr(translatedLanguage.flag):
                    secondLangText = translatedLanguage.flag
                else:
                    secondLangText = translatedLanguage.requireIso6391Code().upper()

                prefixText = f'[ {firstLangText} ➡ {secondLangText} ] '
            elif utils.isValidStr(originalLanguage.flag):
                prefixText = f'[ {originalLanguage.flag} ]'
            else:
                prefixText = f'[ {originalLanguage.requireIso6391Code().upper()} ]'

        return f'{prefixText}{self.__translatedText}'

    @property
    def translationApiSource(self) -> TranslationApiSource:
        return self.__translationApiSource
