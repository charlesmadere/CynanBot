from typing import Any

import CynanBot.misc.utils as utils
from CynanBot.google.googleTranslateTextGlossaryConfig import \
    GoogleTranslateTextGlossaryConfig


class GoogleTranslation():

    def __init__(
        self,
        glossaryConfig: GoogleTranslateTextGlossaryConfig | None,
        detectedLanguageCode: str,
        model: str | None,
        translatedText: str | None
    ):
        if glossaryConfig is not None and not isinstance(glossaryConfig, GoogleTranslateTextGlossaryConfig):
            raise TypeError(f'glossaryConfig argument is malformed: \"{glossaryConfig}\"')
        elif not utils.isValidStr(detectedLanguageCode):
            raise TypeError(f'detectedLanguageCode argument is malformed: \"{detectedLanguageCode}\"')
        elif model is not None and not isinstance(model, str):
            raise TypeError(f'model argument is malformed: \"{model}\"')
        elif translatedText is not None and not isinstance(translatedText, str):
            raise TypeError(f'translatedText argument is malformed: \"{translatedText}\"')

        self.__glossaryConfig: GoogleTranslateTextGlossaryConfig | None = glossaryConfig
        self.__detectedLanguageCode: str = detectedLanguageCode
        self.__model: str | None = model
        self.__translatedText: str | None = translatedText

    def getDetectedLanguageCode(self) -> str:
        return self.__detectedLanguageCode

    def getGlossaryConfig(self) -> GoogleTranslateTextGlossaryConfig | None:
        return self.__glossaryConfig

    def getModel(self) -> str | None:
        return self.__model

    def getTranslatedText(self) -> str | None:
        return self.__translatedText

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'glossaryConfig': self.__glossaryConfig,
            'detectedLanguageCode': self.__detectedLanguageCode,
            'model': self.__model,
            'translatedText': self.__translatedText
        }
