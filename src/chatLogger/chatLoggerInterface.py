from abc import ABC, abstractmethod


class ChatLoggerInterface(ABC):

    @abstractmethod
    def logMessage(
        self,
        bits: int | None,
        chatterUserId: str,
        chatterUserLogin: str,
        message: str,
        twitchChannel: str,
        twitchChannelId: str,
    ):
        pass

    @abstractmethod
    def logRaid(
        self,
        viewers: int,
        raidUserId: str,
        raidUserLogin: str,
        twitchChannel: str,
        twitchChannelId: str,
    ):
        pass

    @abstractmethod
    def start(self):
        pass
