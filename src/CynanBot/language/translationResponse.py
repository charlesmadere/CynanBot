from typing import Optional

import CynanBot.misc.utils as utils
from CynanBot.language.languageEntry import LanguageEntry
from CynanBot.language.translationApiSource import TranslationApiSource


class TranslationResponse():

    def __init__(
        self,
        originalLanguage: Optional[LanguageEntry],
        translatedLanguage: Optional[LanguageEntry],
        originalText: str,
        translatedText: str,
        translationApiSource: TranslationApiSource
    ):
        if originalLanguage is not None and not originalLanguage.hasIso6391Code():
            raise ValueError(f'originalLanguage argument must be either None or have an ISO 639-1 code: \"{originalLanguage}\"')
        if translatedLanguage is not None and not translatedLanguage.hasIso6391Code():
            raise ValueError(f'translatedLanguage argument must be either None or have an ISO 639-1 code: \"{translatedLanguage}\"')
        if not utils.isValidStr(originalText):
            raise ValueError(f'originalText argument is malformed: \"{originalText}\"')
        if not utils.isValidStr(translatedText):
            raise ValueError(f'translatedText argument is malformed: \"{translatedText}\"')
        assert isinstance(translationApiSource, TranslationApiSource), f"malformed {translationApiSource=}"

        self.__originalLanguage: Optional[LanguageEntry] = originalLanguage
        self.__translatedLanguage: Optional[LanguageEntry] = translatedLanguage
        self.__originalText: str = originalText
        self.__translatedText: str = translatedText
        self.__translationApiSource: TranslationApiSource = translationApiSource

    def getOriginalLanguage(self) -> Optional[LanguageEntry]:
        return self.__originalLanguage

    def getOriginalText(self) -> str:
        return self.__originalText

    def getTranslatedLanguage(self) -> Optional[LanguageEntry]:
        return self.__translatedLanguage

    def getTranslatedText(self) -> str:
        return self.__translatedText

    def getTranslationApiSource(self) -> TranslationApiSource:
        return self.__translationApiSource

    def toStr(self) -> str:
        prefixText = ''
        originalLanguage = self.__originalLanguage
        translatedLanguage = self.__translatedLanguage

        if originalLanguage is not None:
            if translatedLanguage is not None:
                firstLangText = ''
                if originalLanguage.hasFlag():
                    firstLangText = originalLanguage.getFlag()
                else:
                    firstLangText = originalLanguage.requireIso6391Code().upper()

                secondLangText = ''
                if translatedLanguage.hasFlag():
                    secondLangText = translatedLanguage.getFlag()
                else:
                    secondLangText = translatedLanguage.requireIso6391Code().upper()

                prefixText = f'[ {firstLangText} ➡ {secondLangText} ] '
            elif originalLanguage.hasFlag():
                prefixText = f'[ {originalLanguage.getFlag()} ]'
            else:
                prefixText = f'[ {originalLanguage.requireIso6391Code().upper()} ]'

        return f'{prefixText}{self.__translatedText}'
