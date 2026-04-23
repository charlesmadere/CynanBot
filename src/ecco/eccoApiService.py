import traceback
from datetime import datetime
from typing import Final

from .eccoApiServiceInterface import EccoApiServiceInterface
from .eccoConstants import EccoConstants
from .eccoResponseParserInterface import EccoResponseParserInterface
from ..misc import utils as utils
from ..network.exceptions import GenericNetworkException
from ..network.networkClientProvider import NetworkClientProvider
from ..timber.timberInterface import TimberInterface


class EccoApiService(EccoApiServiceInterface):

    def __init__(
        self,
        eccoConstants: EccoConstants,
        eccoResponseParser: EccoResponseParserInterface,
        networkClientProvider: NetworkClientProvider,
        timber: TimberInterface,
    ):
        if not isinstance(eccoConstants, EccoConstants):
            raise TypeError(f'eccoConstants argument is malformed: \"{eccoConstants}\"')
        elif not isinstance(eccoResponseParser, EccoResponseParserInterface):
            raise TypeError(f'eccoResponseParser argument is malformed: \"{eccoResponseParser}\"')
        elif not isinstance(networkClientProvider, NetworkClientProvider):
            raise TypeError(f'networkClientProvider argument is malformed: \"{networkClientProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__eccoConstants: Final[EccoConstants] = eccoConstants
        self.__eccoResponseParser: Final[EccoResponseParserInterface] = eccoResponseParser
        self.__networkClientProvider: Final[NetworkClientProvider] = networkClientProvider
        self.__timber: Final[TimberInterface] = timber

    async def fetchEccoTimerDateTime(self) -> datetime:
        self.__timber.log('EccoApiService', f'Fetching Ecco timer datetime...')
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get(
                url = self.__eccoConstants.websiteUrl,
                headers = {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Encoding': 'gzip, deflate, br, zstd',
                    'Accept-Language': 'en-US,en;q=0.9,ja;q=0.8',
                    'Connection': 'keep-alive',
                    'DNT': '1',
                    'Host': 'www.eccothedolphin.com',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'none',
                    'Sec-Fetch-User': '?1',
                    'Sec-GPC': '1',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:150.0) Gecko/20100101 Firefox/150.0',
                },
            )
        except GenericNetworkException as e:
            self.__timber.log('EccoApiService', f'Encountered network error when fetching main Ecco website HTML', e, traceback.format_exc())
            raise GenericNetworkException(f'EccoApiService encountered network error when fetching main Ecco website HTML: {e}')

        htmlString = await response.string()
        await response.close()

        scriptSource = await self.__eccoResponseParser.findTimerScriptSource(
            htmlString = htmlString,
        )

        if not utils.isValidUrl(scriptSource):
            self.__timber.log('EccoApiService', f'Unable to retrieve script source from network response ({response=}) ({scriptSource=})')
            raise GenericNetworkException(f'EccoApiService was unable to retrieve script source from network response ({response=}) ({scriptSource=})')

        try:
            response = await clientSession.get(
                url = scriptSource,
                headers = {
                    'Accept': '*/*',
                    'Accept-Encoding': 'gzip, deflate, br, zstd',
                    'Accept-Language': 'en-US,en;q=0.9,ja;q=0.8',
                    'Connection': 'keep-alive',
                    'DNT': '1',
                    'Host': 'www.eccothedolphin.com',
                    'Referer': 'https://www.eccothedolphin.com/en/',
                    'Sec-Fetch-Dest': 'script',
                    'Sec-Fetch-Mode': 'no-cors',
                    'Sec-Fetch-Site': 'same-origin',
                    'Sec-GPC': '1',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:150.0) Gecko/20100101 Firefox/150.0',
                },
            )
        except GenericNetworkException as e:
            self.__timber.log('EccoApiService', f'Encountered network error when fetching Ecco script file ({scriptSource=})', e, traceback.format_exc())
            raise GenericNetworkException(f'EccoApiService encountered network error when fetching Ecco script file ({scriptSource=}): {e}')

        scriptString = await response.string()
        await response.close()

        timerDateTime = await self.__eccoResponseParser.findTimerDateTimeValue(
            scriptString = scriptString,
        )

        if timerDateTime is None:
            self.__timber.log('EccoApiService', f'Unable to retrieve datetime from Ecco script file ({scriptSource=}) ({response=}) ({timerDateTime=})')
            raise GenericNetworkException(f'EccoApiService was unable to retrieve datetime from Ecco script file ({scriptSource=}) ({response=}) ({timerDateTime=})')

        return timerDateTime
