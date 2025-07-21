from abc import ABC, abstractmethod


class ChatLoggerInterface(ABC):

    @abstractmethod
    def logCheer(
        self,
        bits: int,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str,
        userName: str,
    ):
        pass

    @abstractmethod
    def logMessage(
        self,
        msg: str,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str,
        userName: str,
    ):
        pass

    @abstractmethod
    def logRaid(
        self,
        raidSize: int,
        fromWho: str,
        twitchChannel: str,
        twitchChannelId: str,
    ):
        pass

    @abstractmethod
    def start(self):
        pass
