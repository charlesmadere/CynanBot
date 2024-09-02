from abc import abstractmethod

from .chatterBeanStats import ChatterBeanStats
from ..misc.clearable import Clearable


class BeanStatsRepositoryInterface(Clearable):

    @abstractmethod
    async def get(
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
