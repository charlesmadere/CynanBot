class RedemptionCounterIsDisabledException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class RedemptionCounterNoSuchUserException(Exception):

    def __init__(self, chatterUserId: str, counterName: str, twitchChannelId: str):
        super().__init__(chatterUserId, counterName, twitchChannelId)
