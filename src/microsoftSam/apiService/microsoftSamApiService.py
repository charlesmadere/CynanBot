import traceback
import urllib.parse

from .microsoftSamApiServiceInterface import MicrosoftSamApiServiceInterface
from ...misc import utils as utils
from ...network.exceptions import GenericNetworkException
from ...network.networkClientProvider import NetworkClientProvider
from ...timber.timberInterface import TimberInterface


class MicrosoftSamApiService(MicrosoftSamApiServiceInterface):

    def __init__(
        self,
        networkClientProvider: NetworkClientProvider,
        timber: TimberInterface
    ):
        if not isinstance(networkClientProvider, NetworkClientProvider):
            raise TypeError(f'networkClientProvider argument is malformed: \"{networkClientProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__networkClientProvider: NetworkClientProvider = networkClientProvider
        self.__timber: TimberInterface = timber

    async def getSpeech(self, text: str) -> bytes:
        if not utils.isValidStr(text):
            raise TypeError(f'text argument is malformed: \"{text}\"')

        self.__timber.log('MicrosoftSamApiService', f'Fetching speech... ({text=})')
        clientSession = await self.__networkClientProvider.get()
        text = urllib.parse.quote_plus(text).strip()

        try:
            response = await clientSession.get(
                url = f'https://www.tetyys.com/SAPI4/SAPI4?text={text}&voice=Sam&pitch=100&speed=150'
            )
        except GenericNetworkException as e:
            self.__timber.log('MicrosoftSamApiService', f'Encountered network error when fetching speech ({text=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'MicrosoftSamApiService encountered network error when fetching speech ({text=}): {e}')

        responseStatusCode = response.statusCode
        speechBytes = await response.read()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('MicrosoftSamApiService', f'Encountered non-200 HTTP status code when fetching speech ({text=}) ({response=}) ({responseStatusCode=})')
            raise GenericNetworkException(f'MicrosoftSamApiService encountered non-200 HTTP status code when fetching speech ({text=}) ({response=}) ({responseStatusCode=})')
        elif speechBytes is None:
            self.__timber.log('MicrosoftSamApiService', f'Unable to fetch speech bytes ({text=}) ({response=}) ({responseStatusCode=})')
            raise GenericNetworkException(f'MicrosoftSamApiService unable to fetch speech bytes ({text=}) ({response=}) ({responseStatusCode=})')

        return speechBytes
