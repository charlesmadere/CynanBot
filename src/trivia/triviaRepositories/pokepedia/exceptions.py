class UnsupportedPokepediaMoveTriviaQuestionType(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class UnsupportedPokepediaTriviaQuestionType(Exception):

    def __init__(self, message: str):
        super().__init__(message)
