import traceback
from datetime import datetime
from typing import Any, Final

from .cutenessMapperInterface import CutenessMapperInterface
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class CutenessMapper(CutenessMapperInterface):

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

    async def parseUtcYearAndMonthString(
        self,
        utcYearAndMonthString: str | Any | None,
    ) -> datetime | None:
        if not utils.isValidStr(utcYearAndMonthString):
            return None

        try:
            return datetime.strptime(utcYearAndMonthString, '%Y-%m').replace(
                tzinfo = self.__timeZoneRepository.getDefault()
            )
        except Exception as e:
            self.__timber.log('CutenessMapper', f'Encountered exception when trying to parse the given utcYearAndMonthString ({utcYearAndMonthString=})', e, traceback.format_exc())
            return None

    async def requireUtcYearAndMonthString(
        self,
        utcYearAndMonthString: str | Any | None,
    ) -> datetime:
        result = await self.parseUtcYearAndMonthString(
            utcYearAndMonthString = utcYearAndMonthString,
        )

        if result is None:
            raise ValueError(f'Failed to parse the given utcYearAndMonthString ({utcYearAndMonthString=})')

        return result
