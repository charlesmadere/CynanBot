from datetime import datetime
from typing import Final

from .mostRecentAnivMessageRepositoryInterface import MostRecentAnivMessageRepositoryInterface
from ..models.mostRecentAnivMessage import MostRecentAnivMessage
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class MostRecentAnivMessageRepository(MostRecentAnivMessageRepositoryInterface):

    def __init__(
        self,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository

        self.__cache: Final[dict[str, MostRecentAnivMessage | None]] = dict()

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('MostRecentAnivMessageRepository', 'Caches cleared')

    async def get(
        self,
        twitchChannelId: str,
    ) -> MostRecentAnivMessage | None:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        return self.__cache.get(twitchChannelId, None)

    async def set(
        self,
        message: str | None,
        twitchChannelId: str,
    ):
        if message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        message = utils.cleanStr(message)

        if utils.isValidStr(message):
            self.__cache[twitchChannelId] = MostRecentAnivMessage(
                dateTime = datetime.now(self.__timeZoneRepository.getDefault()),
                message = message,
            )
            self.__timber.log('MostRecentAnivMessageRepository', f'Updated most recent aniv message in \"{twitchChannelId}\"')
        else:
            self.__cache.pop(twitchChannelId, None)
            self.__timber.log('MostRecentAnivMessageRepository', f'Removed most recent aniv message in \"{twitchChannelId}\"')
