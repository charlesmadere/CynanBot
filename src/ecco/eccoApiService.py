import traceback
from datetime import datetime
from typing import Final

from .eccoApiServiceInterface import EccoApiServiceInterface
from .eccoResponseParserInterface import EccoResponseParserInterface
from ..misc import utils as utils
from ..network.exceptions import GenericNetworkException
from ..network.networkClientProvider import NetworkClientProvider
from ..timber.timberInterface import TimberInterface


class EccoApiService(EccoApiServiceInterface):

    def __init__(
        self,
        eccoResponseParser: EccoResponseParserInterface,
        networkClientProvider: NetworkClientProvider,
        timber: TimberInterface,
        websiteUrl: str = 'https://www.eccothedolphin.com/',
    ):
        if not isinstance(eccoResponseParser, EccoResponseParserInterface):
            raise TypeError(f'eccoResponseParser argument is malformed: \"{eccoResponseParser}\"')
        elif not isinstance(networkClientProvider, NetworkClientProvider):
            raise TypeError(f'networkClientProvider argument is malformed: \"{networkClientProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidUrl(websiteUrl):
            raise TypeError(f'websiteUrl argument is malformed: \"{websiteUrl}\"')

        self.__eccoResponseParser: Final[EccoResponseParserInterface] = eccoResponseParser
        self.__networkClientProvider: Final[NetworkClientProvider] = networkClientProvider
        self.__timber: Final[TimberInterface] = timber
        self.__websiteUrl: Final[str] = websiteUrl

    async def fetchEccoTimerDateTime(self) -> datetime:
        self.__timber.log('EccoApiService', f'Fetching Ecco timer datetime...')
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get(self.__websiteUrl)
        except GenericNetworkException as e:
            self.__timber.log('EccoApiService', f'Encountered network error when fetching main Ecco website HTML', e, traceback.format_exc())
            raise GenericNetworkException(f'EccoApiService encountered network error when fetching main Ecco website HTML: {e}')

        htmlString = await response.string()
        await response.close()

        scriptSource = await self.__eccoResponseParser.findTimerScriptSource(htmlString)

        if not utils.isValidUrl(scriptSource):
            self.__timber.log('EccoApiService', f'Unable to retrieve script source from network response ({response=}) ({scriptSource=})')
            raise GenericNetworkException(f'EccoApiService was unable to retrieve script source from network response ({response=}) ({scriptSource=})')

        try:
            response = await clientSession.get(scriptSource)
        except GenericNetworkException as e:
            self.__timber.log('EccoApiService', f'Encountered network error when fetching Ecco script file ({scriptSource=})', e, traceback.format_exc())
            raise GenericNetworkException(f'EccoApiService encountered network error when fetching Ecco script file ({scriptSource=}): {e}')

        scriptString = await response.string()
        await response.close()

        timerDateTime = await self.__eccoResponseParser.findTimerDateTimeValue(scriptString)

        if timerDateTime is None:
            self.__timber.log('EccoApiService', f'Unable to retrieve datetime from Ecco script file ({scriptSource=}) ({response=}) ({timerDateTime=})')
            raise GenericNetworkException(f'EccoApiService was unable to retrieve datetime from Ecco script file ({scriptSource=}) ({response=}) ({timerDateTime=})')

        return timerDateTime
