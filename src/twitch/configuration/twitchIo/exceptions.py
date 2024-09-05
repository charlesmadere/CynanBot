class TwitchIoHasMalformedTagsException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class TwitchIoTagsIsMissingMessageIdException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class TwitchIoTagsIsMissingRoomIdException(Exception):

    def __init__(self, message: str):
        super().__init__(message)
