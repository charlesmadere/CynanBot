class NoTwitchTokenDetailsException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


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

    def __init__(self, message: str):
        super().__init__(message)


class TwitchTokenIsExpiredException(Exception):

    def __init__(self, message: str):
        super().__init__(message)
