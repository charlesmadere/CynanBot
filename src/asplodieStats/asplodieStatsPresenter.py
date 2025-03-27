from .models.asplodieStats import AsplodieStats
from ..misc import utils as utils


class AsplodieStatsPresenter:

    async def printOut(self, asplodieStats: AsplodieStats) -> str:
        if not isinstance(asplodieStats, AsplodieStats):
            raise TypeError(f'asplodieStats argument is malformed: \"{asplodieStats}\"')

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
        return f'{asplodieStats.totalAsplodiesStr} {asplodiesPluralization} with {asplodieStats.selfAsplodiesStr} {selfAsplodiesPluralization} (that\'s {totalDurationAsplodied}!)'
