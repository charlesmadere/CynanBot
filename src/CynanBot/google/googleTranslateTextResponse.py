from typing import Any

from CynanBot.google.googleTranslation import GoogleTranslation


class GoogleTranslateTextResponse():

    def __init__(
        self,
        glossaryTranslations: list[GoogleTranslation] | None = None,
        translations: list[GoogleTranslation] | None = None
    ):
        if glossaryTranslations is not None and not isinstance(glossaryTranslations, list):
            raise TypeError(f'glossaryTranslations argument is malformed: \"{glossaryTranslations}\"')
        elif translations is not None and not isinstance(translations, list):
            raise TypeError(f'translations argument is malformed: \"{translations}\"')

        self.__glossaryTranslations: list[GoogleTranslation] | None = glossaryTranslations
        self.__translations: list[GoogleTranslation] | None = translations

    def getGlossaryTranslations(self) -> list[GoogleTranslation] | None:
        return self.__glossaryTranslations

    def getTranslations(self) -> list[GoogleTranslation] | None:
        return self.__translations

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'glossaryTranslations': self.__glossaryTranslations,
            'translations': self.__translations
        }
