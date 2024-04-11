from typing import Any

from CynanBot.deepL.deepLTranslationResponse import DeepLTranslationResponse


class DeepLTranslationResponses():

    def __init__(
        self,
        translations: list[DeepLTranslationResponse] | None
    ):
        if translations is not None and not isinstance(translations, list):
            raise TypeError(f'translations argument is malformed: \"{translations}\"')

        self.__translations: list[DeepLTranslationResponse] | None = translations

    def getTranslations(self) -> list[DeepLTranslationResponse] | None:
        return self.__translations

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'translations': self.__translations
        }
