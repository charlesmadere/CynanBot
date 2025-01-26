class TwitchIrcTagsAreMalformedException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class TwitchIrcTagsAreMissingMessageIdException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class TwitchIrcTagsAreMissingRoomIdException(Exception):

    def __init__(self, message: str):
        super().__init__(message)

class TwitchIrcTagsAreMissingUserIdException(Exception):

    def __init__(self, message: str):
        super().__init__(message)
