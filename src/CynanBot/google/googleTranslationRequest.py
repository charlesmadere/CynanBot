from typing import Any

import CynanBot.misc.utils as utils
from CynanBot.google.googleTranslateTextGlossaryConfig import \
    GoogleTranslateTextGlossaryConfig
from CynanBot.google.googleTranslateTextTransliterationConfig import \
    GoogleTranslateTextTransliterationConfig


class GoogleTranslationRequest():

    def __init__(
        self,
        glossaryConfig: GoogleTranslateTextGlossaryConfig | None,
        transliterationConfig: GoogleTranslateTextTransliterationConfig | None,
        contents: list[str],
        mimeType: str,
        model: str | None,
        sourceLanguageCode: str | None,
        targetLanguageCode: str,
    ):
        if glossaryConfig is not None and not isinstance(glossaryConfig, GoogleTranslateTextGlossaryConfig):
            raise TypeError(f'glossaryConfig argument is malformed: \"{glossaryConfig}\"')
        elif transliterationConfig is not None and not isinstance(transliterationConfig, GoogleTranslateTextTransliterationConfig):
            raise TypeError(f'transliterationConfig argument is malformed: \"{transliterationConfig}\"')
        elif not isinstance(contents, list):
            raise TypeError(f'contents argument is malformed: \"{contents}\"')
        elif not utils.isValidStr(mimeType):
            raise TypeError(f'mimeType argument is malformed: \"{mimeType}\"')
        elif model is not None and not isinstance(model, str):
            raise TypeError(f'model argument is malformed: \"{model}\"')
        elif sourceLanguageCode is not None and not isinstance(sourceLanguageCode, str):
            raise TypeError(f'sourceLanguageCode argument is malformed: \"{sourceLanguageCode}\"')
        elif not utils.isValidStr(targetLanguageCode):
            raise TypeError(f'targetLanguageCode argument is malformed: \"{targetLanguageCode}\"')

        self.__glossaryConfig: GoogleTranslateTextGlossaryConfig | None = glossaryConfig
        self.__transliterationConfig: GoogleTranslateTextTransliterationConfig | None = transliterationConfig
        self.__contents: list[str] = contents
        self.__mimeType: str = mimeType
        self.__model: str | None = model
        self.__sourceLanguageCode: str | None = sourceLanguageCode
        self.__targetLanguageCode: str = targetLanguageCode

    def getContents(self) -> list[str]:
        return self.__contents

    def getGlossaryConfig(self) -> GoogleTranslateTextGlossaryConfig | None:
        return self.__glossaryConfig

    def getMimeType(self) -> str:
        return self.__mimeType

    def getModel(self) -> str | None:
        return self.__model

    def getSourceLanguageCode(self) -> str | None:
        return self.__sourceLanguageCode

    def getTargetLanguageCode(self) -> str:
        return self.__targetLanguageCode

    def getTransliterationConfig(self) -> GoogleTranslateTextTransliterationConfig | None:
        return self.__transliterationConfig

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'contents': self.__contents,
            'glossaryConfig': self.__glossaryConfig,
            'mimeType': self.__mimeType,
            'model': self.__model,
            'sourceLanguageCode': self.__sourceLanguageCode,
            'targetLanguageCode': self.__targetLanguageCode,
            'transliterationConfig': self.__transliterationConfig
        }
