from .beanStatsRepositoryInterface import BeanStatsRepositoryInterface
from .chatterBeanStats import ChatterBeanStats
from ..storage.backingDatabase import BackingDatabase
from ..timber.timberInterface import TimberInterface


class BeanStatsRepository(BeanStatsRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__timber: TimberInterface = timber

        self.__isDatabaseReady: bool = False

    async def clearCaches(self):
        # TODO
        self.__timber.log('BeanStatsRepository', f'Caches cleared')

    async def get(
        self,
        chatterUserId: str,
        chatterUserName: str,
        twitchChannel: str,
        twitchChannelId: str
    ) -> ChatterBeanStats | None:
        # TODO
        return None

    async def incrementFails(
        self,
        chatterUserId: str,
        chatterUserName: str,
        twitchChannel: str,
        twitchChannelId: str
    ) -> ChatterBeanStats:
        # TODO
        raise RuntimeError()

    async def incrementSuccesses(
        self,
        chatterUserId: str,
        chatterUserName: str,
        twitchChannel: str,
        twitchChannelId: str
    ) -> ChatterBeanStats:
        # TODO
        raise RuntimeError()
