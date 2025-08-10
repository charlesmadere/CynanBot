from datetime import datetime
from typing import Final

from frozendict import frozendict

from .mostRecentAnivMessageRepositoryInterface import MostRecentAnivMessageRepositoryInterface
from ..models.mostRecentAnivMessage import MostRecentAnivMessage
from ..models.whichAnivUser import WhichAnivUser
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

        self.__cache: Final[dict[str, dict[WhichAnivUser, MostRecentAnivMessage | None]]] = dict()

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('MostRecentAnivMessageRepository', 'Caches cleared')

    async def get(
        self,
        twitchChannelId: str,
    ) -> frozendict[WhichAnivUser, MostRecentAnivMessage | None]:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        return frozendict(self.__cache.get(twitchChannelId, None))

    async def set(
        self,
        message: str | None,
        twitchChannelId: str,
        whichAnivUser: WhichAnivUser,
    ):
        if message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not isinstance(whichAnivUser, WhichAnivUser):
            raise TypeError(f'whichAnivUser argument is malformed: \"{whichAnivUser}\"')

        cleanedMessage = utils.cleanStr(message)

        if utils.isValidStr(cleanedMessage):
            self.__cache[twitchChannelId][whichAnivUser] = MostRecentAnivMessage(
                dateTime = datetime.now(self.__timeZoneRepository.getDefault()),
                message = cleanedMessage,
                whichAnivUser = whichAnivUser,
            )
            self.__timber.log('MostRecentAnivMessageRepository', f'Updated most recent aniv message ({twitchChannelId=}) ({whichAnivUser=})')
        else:
            self.__cache[twitchChannelId].pop(whichAnivUser, None)
            self.__timber.log('MostRecentAnivMessageRepository', f'Removed most recent aniv message ({twitchChannelId=}) ({whichAnivUser=})')
