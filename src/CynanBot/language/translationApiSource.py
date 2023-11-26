from enum import Enum, auto


class TranslationApiSource(Enum):

    DEEP_L = auto()
    GOOGLE_TRANSLATE = auto()

    def isEnabled(self) -> bool:
        if self is TranslationApiSource.DEEP_L:
            return True
        elif self is TranslationApiSource.GOOGLE_TRANSLATE:
            return True
        else:
            raise ValueError(f'unknown TriviaSource: \"{self}\"')
