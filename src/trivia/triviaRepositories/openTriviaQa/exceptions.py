class NoTriviaIncorrectAnswersException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class NoTriviaQuestionsAvailableException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class TriviaDatabaseFileDoesNotExistException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class UnknownOpenTriviaQaQuestionTypeException(Exception):

    def __init__(self, message: str):
        super().__init__(message)
