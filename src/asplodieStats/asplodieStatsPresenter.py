import math
from typing import Final

from .models.asplodieStats import AsplodieStats


class AsplodieStatsPresenter:

    MINUTE_IN_SECONDS: Final[int] = 60
    HOUR_IN_SECONDS: Final[int] = 3600
    DAY_IN_SECONDS: Final[int] = 86400
    WEEK_IN_SECONDS: Final[int] = 604800

    async def __determineAsplodiedDuration(self, asplodiedDuration: int) -> str:
        weeks = math.floor(asplodiedDuration / self.WEEK_IN_SECONDS)
        if weeks >= 1:
            asplodiedDuration = asplodiedDuration - (weeks * self.WEEK_IN_SECONDS)

        days = math.floor(asplodiedDuration / self.DAY_IN_SECONDS)
        if days >= 1:
            asplodiedDuration = asplodiedDuration - (days * self.DAY_IN_SECONDS)

        hours = math.floor(asplodiedDuration / self.HOUR_IN_SECONDS)
        if hours >= 1:
            asplodiedDuration = asplodiedDuration - (hours * self.HOUR_IN_SECONDS)

        minutes = math.floor(asplodiedDuration / self.MINUTE_IN_SECONDS)
        if minutes >= 1:
            asplodiedDuration = asplodiedDuration - (minutes * self.MINUTE_IN_SECONDS)

        # the only value now remaining in asplodiedDuration is the number of seconds
        seconds = asplodiedDuration

        weeksString = ''
        if weeks == 1:
            weeksString = 'week'
        elif weeks > 1:
            weeksString = 'weeks'

        daysString = ''
        if days == 1:
            daysString = 'day'
        elif days > 1:
            daysString = 'days'

        hoursString = ''
        if hours == 1:
            hoursString = 'hour'
        elif hours > 1:
            hoursString = 'hours'

        minutesString = ''
        if minutes == 1:
            minutesString = 'minute'
        elif minutes > 1:
            minutesString = 'minutes'

        secondsString = ''
        if seconds == 1:
            secondsString = 'second'
        elif seconds > 1:
            secondsString = 'seconds'

        # TODO
        return f'{weeksString} {daysString} {hoursString} {minutesString} {secondsString}'

    async def printOut(self, asplodieStats: AsplodieStats) -> str:
        if not isinstance(asplodieStats, AsplodieStats):
            raise TypeError(f'asplodieStats argument is malformed: \"{asplodieStats}\"')

        asplodiesPluralization: str
        if asplodieStats.totalAsplodies == 1:
            asplodiesPluralization = 'asplodie'
        else:
            asplodiesPluralization = 'asplodies'

        totalDurationAsplodied = await self.__determineAsplodiedDuration(asplodieStats.totalDurationAsplodiedSeconds)
        return f'{asplodieStats.totalAsplodiesStr} {asplodiesPluralization} (that\'s {totalDurationAsplodied}!)'
