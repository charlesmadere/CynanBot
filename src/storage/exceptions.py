class DatabaseConnectionIsClosedException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class DatabaseOperationalError(Exception):

    def __init__(self, message: str):
        super().__init__(message)
