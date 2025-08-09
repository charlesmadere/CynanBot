from ..models.asplodieStats import AsplodieStats
from ..repository.asplodieStatsRepositoryInterface import AsplodieStatsRepositoryInterface
from ...misc import utils as utils


class StubAsplodieStatsRepository(AsplodieStatsRepositoryInterface):

    async def addAsplodie(
        self,
        isSelfAsplodie: bool,
        durationAsplodiedSeconds: int,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> AsplodieStats:
        if not utils.isValidBool(isSelfAsplodie):
            raise TypeError(f'isSelfAsplodie argument is malformed: \"{isSelfAsplodie}\"')
        elif not utils.isValidInt(durationAsplodiedSeconds):
            raise TypeError(f'durationAsplodiedSeconds argument is malformed: \"{durationAsplodiedSeconds}\"')
        elif not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        return await self.get(
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId,
        )

    async def clearCaches(self):
        # this method is intentionally empty
        pass

    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> AsplodieStats:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        return AsplodieStats(
            selfAsplodies = 0,
            totalAsplodies = 0,
            totalDurationAsplodiedSeconds = 0,
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId,
        )
