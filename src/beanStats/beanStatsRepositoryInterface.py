from abc import ABC, abstractmethod

from .chatterBeanStats import ChatterBeanStats


class BeanStatsRepositoryInterface(ABC):

    @abstractmethod
    async def getStats(
        self,
        chatterUserId: str,
        chatterUserName: str,
        twitchChannel: str,
        twitchChannelId: str
    ) -> ChatterBeanStats | None:
        pass

    @abstractmethod
    async def incrementFails(
        self,
        chatterUserId: str,
        chatterUserName: str,
        twitchChannel: str,
        twitchChannelId: str
    ) -> ChatterBeanStats:
        pass

    @abstractmethod
    async def incrementSuccesses(
        self,
        chatterUserId: str,
        chatterUserName: str,
        twitchChannel: str,
        twitchChannelId: str
    ) -> ChatterBeanStats:
        pass
