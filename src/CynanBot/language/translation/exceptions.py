from CynanBot.language.translationApiSource import TranslationApiSource


class TranslationEngineUnavailableException(Exception):

    def __init__(
        self,
        message: str,
        translationApiSource: TranslationApiSource
    ):
        assert isinstance(message, str), f"malformed {message=}"
        assert isinstance(translationApiSource, TranslationApiSource), f"malformed {translationApiSource=}"

        super().__init__(message, translationApiSource)


class TranslationException(Exception):

    def __init__(
        self,
        message: str,
        translationApiSource: TranslationApiSource
    ):
        assert isinstance(message, str), f"malformed {message=}"
        assert isinstance(translationApiSource, TranslationApiSource), f"malformed {translationApiSource=}"

        super().__init__(message, translationApiSource)
