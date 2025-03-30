from .models.asplodieStats import AsplodieStats
from ..misc import utils as utils


class AsplodieStatsPresenter:

    async def printOut(
        self,
        asplodieStats: AsplodieStats,
        chatterUserName: str
    ) -> str:
        if not isinstance(asplodieStats, AsplodieStats):
            raise TypeError(f'asplodieStats argument is malformed: \"{asplodieStats}\"')
        elif not utils.isValidStr(chatterUserName):
            raise TypeError(f'chatterUserName argument is malformed: \"{chatterUserName}\"')

        asplodiesPluralization: str
        if asplodieStats.totalAsplodies == 1:
            asplodiesPluralization = 'asplodie'
        else:
            asplodiesPluralization = 'asplodies'

        selfAsplodiesPluralization: str
        if asplodieStats.selfAsplodies == 1:
            selfAsplodiesPluralization = 'self asplodie'
        else:
            selfAsplodiesPluralization = 'self asplodies'

        totalDurationAsplodied = utils.secondsToDurationMessage(asplodieStats.totalDurationAsplodiedSeconds)
        return f'{asplodieStats.totalAsplodiesStr} {asplodiesPluralization}; {asplodieStats.selfAsplodiesStr} {selfAsplodiesPluralization} (that\'s {totalDurationAsplodied}!)'
