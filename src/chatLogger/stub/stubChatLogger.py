from ..chatLoggerInterface import ChatLoggerInterface


class StubChatLogger(ChatLoggerInterface):

    def logCheer(
        self,
        bits: int,
        cheerUserId: str,
        cheerUserLogin: str,
        twitchChannel: str,
        twitchChannelId: str,
    ):
        # this method is intentionally empty
        pass

    def logMessage(
        self,
        bits: int | None,
        chatterUserId: str,
        chatterUserLogin: str,
        message: str,
        twitchChannel: str,
        twitchChannelId: str,
    ):
        # this method is intentionally empty
        pass

    def logRaid(
        self,
        viewers: int,
        raidUserId: str,
        raidUserLogin: str,
        twitchChannel: str,
        twitchChannelId: str,
    ):
        # this method is intentionally empty
        pass

    def start(self):
        # this method is intentionally empty
        pass
