from datetime import datetime

from ..supStreamerChatter import SupStreamerChatter
from ..supStreamerRepositoryInterface import SupStreamerRepositoryInterface
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils


class StubSupStreamerRepository(SupStreamerRepositoryInterface):

    def __init__(self, timeZoneRepository: TimeZoneRepositoryInterface):
        if not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')

        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository

    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ) -> SupStreamerChatter | None:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        now = datetime.now(self.__timeZoneRepository.getDefault())

        return SupStreamerChatter(
            mostRecentSup = now,
            twitchChannelId = twitchChannelId,
            userId = chatterUserId
        )

    async def set(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ):
        # this method is intentionally empty
        pass
