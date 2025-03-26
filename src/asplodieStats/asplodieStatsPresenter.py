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

        totalDurationAsplodied = utils.secondsToDurationMessage(asplodieStats.totalDurationAsplodiedSeconds)
        return f'{asplodieStats.totalAsplodiesStr} {asplodiesPluralization} (that\'s {totalDurationAsplodied}!)'
