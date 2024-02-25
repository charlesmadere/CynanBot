from typing import Optional

from CynanBot.google.googleTranslateGlossaryConfig import \
    GoogleTranslateGlossaryConfig


class GoogleTranslateTextEntry():

    def __init__(
        self,
        glossaryConfig: GoogleTranslateGlossaryConfig,
        detectedLanguageCode: Optional[str],
        model: Optional[str],
        translatedText: Optional[str]
    ):
        if not isinstance(glossaryConfig, GoogleTranslateGlossaryConfig):
            raise TypeError(f'glossaryConfig argument is malformed: \"{glossaryConfig}\"')
        elif detectedLanguageCode is None and not isinstance(detectedLanguageCode, str):
            raise TypeError(f'detectedLanguageCode argument is malformed: \"{detectedLanguageCode}\"')
        elif model is not None and not isinstance(model, str):
            raise TypeError(f'model argument is malformed: \"{model}\"')
        elif not isinstance(translatedText, str):
            raise TypeError(f'translatedText argument is malformed: \"{translatedText}\"')

        self.__glossaryConfig: GoogleTranslateGlossaryConfig = glossaryConfig
        self.__detectedLanguageCode: Optional[str] = detectedLanguageCode
        self.__model: Optional[str] = model
        self.__translatedText: Optional[str] = translatedText


