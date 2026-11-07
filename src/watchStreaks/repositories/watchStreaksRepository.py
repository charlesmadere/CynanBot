from typing import Final

from src.watchStreaks.models.watchStreakStats import WatchStreakStats

from .watchStreaksRepositoryInterface import WatchStreaksRepositoryInterface
from ...misc import utils as utils
from ...storage.backingDatabase import BackingDatabase
from ...timber.timberInterface import TimberInterface


class WatchStreaksRepository(WatchStreaksRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__backingDatabase: Final[BackingDatabase] = backingDatabase
        self.__timber: Final[TimberInterface] = timber

    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> WatchStreakStats | None:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        # TODO
        raise RuntimeError()

    async def update(
        self,
        currentStreak: int,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> WatchStreakStats:
        if not utils.isValidInt(currentStreak):
            raise TypeError(f'currentStreak argument is malformed: \"{currentStreak}\"')
        elif currentStreak < 0 or currentStreak > utils.getIntMaxSafeSize():
            raise ValueError(f'currentStreak argument is out of bounds" {currentStreak}')
        elif not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        # TODO
        raise RuntimeError()
