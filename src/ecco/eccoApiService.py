import traceback
from typing import Final

from .eccoApiServiceInterface import EccoApiServiceInterface
from ..misc import utils as utils
from ..network.exceptions import GenericNetworkException
from ..network.networkClientProvider import NetworkClientProvider
from ..timber.timberInterface import TimberInterface


class EccoApiService(EccoApiServiceInterface):

    def __init__(
        self,
        networkClientProvider: NetworkClientProvider,
        timber: TimberInterface
    ):
        if not isinstance(networkClientProvider, NetworkClientProvider):
            raise TypeError(f'networkClientProvider argument is malformed: \"{networkClientProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__networkClientProvider: Final[NetworkClientProvider] = networkClientProvider
        self.__timber: Final[TimberInterface] = timber

    async def fetchEccoWebsiteHtmlString(self) -> str:
        self.__timber.log('EccoApiService', f'Fetching Ecco website HTML...')
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get('http://www.eccothedolphin.com/')
        except GenericNetworkException as e:
            self.__timber.log('EccoApiService', f'Encountered network error when fetching Ecco website: {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'EccoApiService encountered network error when fetching Ecco website: {e}')

        htmlString = await response.string()

        if not utils.isValidStr(htmlString):
            raise GenericNetworkException(f'EccoApiService was unable to retrieve HTML string from network response ({response=}) ({htmlString=})')

        return htmlString
