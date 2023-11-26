from typing import Optional

from CynanBot.trivia.triviaSource import TriviaSource
from CynanBot.trivia.triviaType import TriviaType


class AdditionalTriviaAnswerAlreadyExistsException(Exception):

    def __init__(
        self,
        message: str,
        triviaId: str,
        triviaSource: TriviaSource,
        triviaType: TriviaType
    ):
        super().__init__(message, triviaId, triviaSource, triviaType)


class AdditionalTriviaAnswerIsMalformedException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class AdditionalTriviaAnswerIsUnsupportedTriviaTypeException(Exception):

    def __init__(self, message: str, triviaType: TriviaType, triviaSource: TriviaSource):
        super().__init__(message, triviaType, triviaSource)


class BadTriviaAnswerException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class BadTriviaDifficultyException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class BadTriviaIdException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class BadTriviaSessionTokenException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class BadTriviaSourceException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class BadTriviaTypeException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class GenericTriviaNetworkException(Exception):

    def __init__(
        self,
        triviaSource: TriviaSource,
        exception: Optional[Exception] = None
    ):
        super().__init__(triviaSource, exception)


class MalformedTriviaJsonException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class NoTriviaCorrectAnswersException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class NoTriviaMultipleChoiceResponsesException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class NoTriviaQuestionException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class TooManyAdditionalTriviaAnswersException(Exception):

    def __init__(
        self,
        answerCount: int,
        triviaId: str,
        triviaSource: TriviaSource,
        triviaType: TriviaType
    ):
        super().__init__(answerCount, triviaId, triviaSource, triviaType)


class TooManyTriviaFetchAttemptsException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class UnknownTriviaActionTypeException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class UnknownTriviaGameTypeException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class UnsupportedTriviaTypeException(Exception):

    def __init__(self, message: str):
        super().__init__(message)
