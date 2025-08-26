import math
import traceback
from datetime import datetime
from typing import Final

from .eccoApiServiceInterface import EccoApiServiceInterface
from .eccoHelperInterface import EccoHelperInterface
from .exceptions import EccoFailedToFetchTimeRemaining
from .models.absEccoTimeRemaining import AbsEccoTimeRemaining
from .models.eccoReleased import EccoReleased
from .models.eccoTimeRemaining import EccoTimeRemaining
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..network.exceptions import GenericNetworkException
from ..timber.timberInterface import TimberInterface


class EccoHelper(EccoHelperInterface):

    def __init__(
        self,
        eccoApiService: EccoApiServiceInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
    ):
        if not isinstance(eccoApiService, EccoApiServiceInterface):
            raise TypeError(f'eccoApiService argument is malformed: \"{eccoApiService}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')

        self.__eccoApiService: Final[EccoApiServiceInterface] = eccoApiService
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository

    async def fetchEccoTimeRemaining(self) -> AbsEccoTimeRemaining:
        try:
            timerDateTime = await self.__eccoApiService.fetchEccoTimerDateTime()
        except GenericNetworkException as e:
            self.__timber.log('EccoHelper', f'Failed to fetch Ecco timer datetime value: {e}', e, traceback.format_exc())
            raise EccoFailedToFetchTimeRemaining(f'Failed to fetch Ecco timer datetime value: {e}')

        now = datetime.now(self.__timeZoneRepository.getDefault())
        remainingSeconds = math.floor((timerDateTime - now).total_seconds())

        if remainingSeconds <= 10:
            return EccoReleased()
        else:
            return EccoTimeRemaining(
                timerDateTime = timerDateTime,
                remainingSeconds = remainingSeconds,
            )
