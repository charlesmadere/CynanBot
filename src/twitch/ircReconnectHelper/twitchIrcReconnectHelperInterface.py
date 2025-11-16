from abc import ABC, abstractmethod

from twitchio.ext.commands.bot import Bot


class TwitchIrcReconnectHelperInterface(ABC):

    @abstractmethod
    def setTwitchIoBot(self, twitchIoBot: Bot):
        pass

    @abstractmethod
    def start(self):
        pass
