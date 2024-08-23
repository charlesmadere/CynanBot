from .questions.triviaQuestionType import TriviaQuestionType
from .questions.triviaSource import TriviaSource


class AdditionalTriviaAnswerAlreadyExistsException(Exception):

    def __init__(
        self,
        message: str,
        triviaId: str,
        triviaQuestionType: TriviaQuestionType,
        triviaSource: TriviaSource
    ):
        super().__init__(message, triviaId, triviaQuestionType, triviaSource)


class AdditionalTriviaAnswerIsMalformedException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class AdditionalTriviaAnswerIsUnsupportedTriviaTypeException(Exception):

    def __init__(
        self,
        message: str,
        triviaQuestionType: TriviaQuestionType,
        triviaSource: TriviaSource
    ):
        super().__init__(message, triviaQuestionType, triviaSource)


class BadTriviaAnswerException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class BadTriviaCategoryException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class BadTriviaCategoryIdException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class BadTriviaDifficultyException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class BadTriviaIdException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class BadTriviaOriginalCorrectAnswersException(Exception):

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
        exception: Exception | None = None
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
        triviaQuestionType: TriviaQuestionType,
        triviaSource: TriviaSource
    ):
        super().__init__(answerCount, triviaId, triviaQuestionType, triviaSource)


class TooManyTriviaFetchAttemptsException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class UnavailableTriviaSourceException(Exception):

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
