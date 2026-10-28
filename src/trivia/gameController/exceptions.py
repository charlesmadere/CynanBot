class TriviaGameControllerAlreadyBannedException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class TriviaGameControllerAlreadyExistsException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class TriviaGameControllerDoesNotExistException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class TriviaGameControllerIllegalUserIdException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class TriviaGameControllerNotAlreadyBannedException(Exception):

    def __init__(self, message: str):
        super().__init__(message)
