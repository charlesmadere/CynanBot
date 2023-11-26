import misc.utils as utils
from language.languageEntry import LanguageEntry
from language.translationApiSource import TranslationApiSource


class TranslationResponse():

    def __init__(
        self,
        originalLanguage: LanguageEntry,
        translatedLanguage: LanguageEntry,
        originalText: str,
        translatedText: str,
        translationApiSource: TranslationApiSource
    ):
        if originalLanguage is not None and not originalLanguage.hasIso6391Code():
            raise ValueError(f'originalLanguage argument must be either None or have an ISO 639-1 code: \"{originalLanguage}\"')
        elif translatedLanguage is not None and not translatedLanguage.hasIso6391Code():
            raise ValueError(f'translatedLanguage argument must be either None or have an ISO 639-1 code: \"{translatedLanguage}\"')
        elif not utils.isValidStr(originalText):
            raise ValueError(f'originalText argument is malformed: \"{originalText}\"')
        elif not utils.isValidStr(translatedText):
            raise ValueError(f'translatedText argument is malformed: \"{translatedText}\"')
        elif translationApiSource is None:
            raise ValueError(f'translationApiSource argument is malformed: \"{translationApiSource}\"')

        self.__originalLanguage: LanguageEntry = originalLanguage
        self.__translatedLanguage: LanguageEntry = translatedLanguage
        self.__originalText: str = originalText
        self.__translatedText: str = translatedText
        self.__translationApiSource: TranslationApiSource = translationApiSource

    def getOriginalLanguage(self) -> LanguageEntry:
        return self.__originalLanguage

    def getOriginalText(self) -> str:
        return self.__originalText

    def getTranslatedLanguage(self) -> LanguageEntry:
        return self.__translatedLanguage

    def getTranslatedText(self) -> str:
        return self.__translatedText

    def getTranslationApiSource(self) -> TranslationApiSource:
        return self.__translationApiSource

    def hasOriginalLanguage(self) -> bool:
        return self.__originalLanguage is not None

    def hasTranslatedLanguage(self) -> bool:
        return self.__translatedLanguage is not None

    def toStr(self) -> str:
        prefixText = ''

        if self.hasOriginalLanguage():
            if self.hasTranslatedLanguage():
                firstLangText = ''
                if self.__originalLanguage.hasFlag():
                    firstLangText = self.__originalLanguage.getFlag()
                else:
                    firstLangText = self.__originalLanguage.getIso6391Code().upper()

                secondLangText = ''
                if self.__translatedLanguage.hasFlag():
                    secondLangText = self.__translatedLanguage.getFlag()
                else:
                    secondLangText = self.__translatedLanguage.getIso6391Code().upper()

                prefixText = f'[ {firstLangText} ➡ {secondLangText} ] '
            elif self.__originalLanguage.hasFlag():
                prefixText = f'[ {self.__originalLanguage.getFlag()} ]'
            else:
                prefixText = f'[ {self.__originalLanguage.getIso6391Code().upper()} ]'

        return f'{prefixText}{self.__translatedText}'
