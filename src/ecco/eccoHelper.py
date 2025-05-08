import traceback
from datetime import datetime
from typing import Final

from .eccoApiServiceInterface import EccoApiServiceInterface
from .eccoHelperInterface import EccoHelperInterface
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
        timeZoneRepository: TimeZoneRepositoryInterface
    ):
        self.__eccoApiService: Final[EccoApiServiceInterface] = eccoApiService
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository

    async def getEccoTimeRemaining(self) -> AbsEccoTimeRemaining:
        try:
            timerDateTime = await self.__eccoApiService.fetchEccoTimerDateTime()
        except GenericNetworkException as e:
            self.__timber.log('EccoHelper', f'Failed to fetch timer datetime value: {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'EccoHelper failed to fetch timer datetime value: {e}')

        now = datetime.now(self.__timeZoneRepository.getDefault())
        remainingSeconds = round((timerDateTime - now).total_seconds())

        if remainingSeconds <= 10:
            return EccoReleased()
        else:
            return EccoTimeRemaining(
                timerDateTime = timerDateTime,
                remainingSeconds = remainingSeconds
            )
