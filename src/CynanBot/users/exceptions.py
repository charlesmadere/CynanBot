class NoSuchUserException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class NoUsersException(Exception):

    def __init__(self, message: str):
        super().__init__(message)
