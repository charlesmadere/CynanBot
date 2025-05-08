import traceback
from typing import Final

from .eccoApiServiceInterface import EccoApiServiceInterface
from .eccoResponseParserInterface import EccoResponseParserInterface
from .models.eccoTimerData import EccoTimerData
from ..network.exceptions import GenericNetworkException
from ..network.networkClientProvider import NetworkClientProvider
from ..timber.timberInterface import TimberInterface


class EccoApiService(EccoApiServiceInterface):

    def __init__(
        self,
        eccoResponseParser: EccoResponseParserInterface,
        networkClientProvider: NetworkClientProvider,
        timber: TimberInterface
    ):
        if not isinstance(eccoResponseParser, EccoResponseParserInterface):
            raise TypeError(f'eccoResponseParser argument is malformed: \"{eccoResponseParser}\"')
        elif not isinstance(networkClientProvider, NetworkClientProvider):
            raise TypeError(f'networkClientProvider argument is malformed: \"{networkClientProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__eccoResponseParser: Final[EccoResponseParserInterface] = eccoResponseParser
        self.__networkClientProvider: Final[NetworkClientProvider] = networkClientProvider
        self.__timber: Final[TimberInterface] = timber

    async def fetchEccoTimerData(self) -> EccoTimerData:
        self.__timber.log('EccoApiService', f'Fetching Ecco website...')
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get('https://www.eccothedolphin.com/')
        except GenericNetworkException as e:
            self.__timber.log('EccoApiService', f'Encountered network error when fetching Ecco website: {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'EccoApiService encountered network error when fetching Ecco website: {e}')

        htmlString = await response.string()
        timerData = await self.__eccoResponseParser.parseTimerData(htmlString)
        await response.close()

        if timerData is None:
            self.__timber.log('EccoApiService', f'Unable to retrieve timer data from network response ({response=}) ({timerData=})')
            raise GenericNetworkException(f'EccoApiService was unable to retrieve timer data from network response ({response=}) ({timerData=})')

        return timerData
