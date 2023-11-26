from abc import ABC, abstractmethod


class ChatLoggerInterface(ABC):

    @abstractmethod
    def logMessage(self, msg: str, twitchChannel: str, userId: str, userName: str):
        pass

    @abstractmethod
    def logRaid(self, raidSize: int, fromWho: str, twitchChannel: str):
        pass

    @abstractmethod
    def start(self):
        pass
