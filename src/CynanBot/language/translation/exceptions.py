from CynanBot.language.translationApiSource import TranslationApiSource


class TranslationEngineUnavailableException(Exception):

    def __init__(
        self,
        message: str,
        translationApiSource: TranslationApiSource
    ):
        if not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not isinstance(translationApiSource, TranslationApiSource):
            raise TypeError(f'translationApiSource argument is malformed: \"{translationApiSource}\"')

        super().__init__(message, translationApiSource)


class TranslationException(Exception):

    def __init__(
        self,
        message: str,
        translationApiSource: TranslationApiSource
    ):
        if not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not isinstance(translationApiSource, TranslationApiSource):
            raise TypeError(f'translationApiSource argument is malformed: \"{translationApiSource}\"')

        super().__init__(message, translationApiSource)
