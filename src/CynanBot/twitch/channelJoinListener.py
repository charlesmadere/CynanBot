from abc import ABC, abstractmethod

from twitch.absChannelJoinEvent import AbsChannelJoinEvent


class ChannelJoinListener(ABC):

    @abstractmethod
    async def onNewChannelJoinEvent(self, event: AbsChannelJoinEvent):
        pass
