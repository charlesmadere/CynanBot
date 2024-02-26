from typing import Any, Dict, Optional

from CynanBot.google.googleTranslateTextGlossaryConfig import \
    GoogleTranslateTextGlossaryConfig


class GoogleTranslation():

    def __init__(
        self,
        glossaryConfig: GoogleTranslateTextGlossaryConfig,
        detectedLanguageCode: Optional[str],
        model: Optional[str],
        translatedText: Optional[str]
    ):
        if not isinstance(glossaryConfig, GoogleTranslateTextGlossaryConfig):
            raise TypeError(f'glossaryConfig argument is malformed: \"{glossaryConfig}\"')
        elif detectedLanguageCode is None and not isinstance(detectedLanguageCode, str):
            raise TypeError(f'detectedLanguageCode argument is malformed: \"{detectedLanguageCode}\"')
        elif model is not None and not isinstance(model, str):
            raise TypeError(f'model argument is malformed: \"{model}\"')
        elif not isinstance(translatedText, str):
            raise TypeError(f'translatedText argument is malformed: \"{translatedText}\"')

        self.__glossaryConfig: GoogleTranslateTextGlossaryConfig = glossaryConfig
        self.__detectedLanguageCode: Optional[str] = detectedLanguageCode
        self.__model: Optional[str] = model
        self.__translatedText: Optional[str] = translatedText

    def getDetectedLanguageCode(self) -> Optional[str]:
        return self.__detectedLanguageCode

    def getGlossaryConfig(self) -> GoogleTranslateTextGlossaryConfig:
        return self.__glossaryConfig

    def getModel(self) -> Optional[str]:
        return self.__model

    def getTranslatedText(self) -> Optional[str]:
        return self.__translatedText

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'glossaryConfig': self.__glossaryConfig,
            'detectedLanguageCode': self.__detectedLanguageCode,
            'model': self.__model,
            'translatedText': self.__translatedText
        }
