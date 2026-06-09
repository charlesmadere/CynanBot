class FailedToFindTwitchChannelInformationException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class FailedToFindTwitchGameException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class FailedToSetTwitchChannelGameException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class FailedToSetTwitchChannelTitleException(Exception):

    def __init__(self, message: str):
        super().__init__(message)
