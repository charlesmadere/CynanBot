from typing import Final

from .twitchTokensStorageInterface import TwitchTokensStorageInterface
from ..localModels.twitchTokensDetails import TwitchTokensDetails
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...storage.backingDatabase import BackingDatabase
from ...timber.timberInterface import TimberInterface


class TwitchTokensStorage(TwitchTokensStorageInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')

        self.__backingDatabase: Final[BackingDatabase] = backingDatabase
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository

    async def get(
        self,
        twitchChannelId: str,
    ) -> TwitchTokensDetails | None:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        # TODO
        return None

    async def remove(
        self,
        twitchChannelId: str,
    ):
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        # TODO
        pass

    async def set(
        self,
        twitchChannelId: str,
        twitchTokensDetails: TwitchTokensDetails | None,
    ):
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if twitchTokensDetails is None:
            await self.remove(
                twitchChannelId = twitchChannelId,
            )
            return

        # TODO
        pass
