class TimeoutDurationSecondsTooLongException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class TwitchAccessTokenMissingException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class TwitchErrorException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class TwitchJsonException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class TwitchPasswordChangedException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class TwitchRefreshTokenMissingException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class TwitchStatusCodeException(Exception):

    def __init__(self, statusCode: int, message: str):
        super().__init__(statusCode, message)
        self.__statusCode: int = statusCode

    @property
    def statusCode(self) -> int:
        return self.__statusCode


class TwitchTokenIsExpiredException(Exception):

    def __init__(self, message: str):
        super().__init__(message)
