import traceback
import urllib.parse
from typing import Final

from .streamElementsApiServiceInterface import StreamElementsApiServiceInterface
from ..models.streamElementsVoice import StreamElementsVoice
from ...misc import utils as utils
from ...network.exceptions import GenericNetworkException
from ...network.networkClientProvider import NetworkClientProvider
from ...timber.timberInterface import TimberInterface


class StreamElementsApiService(StreamElementsApiServiceInterface):

    def __init__(
        self,
        networkClientProvider: NetworkClientProvider,
        timber: TimberInterface,
    ):
        if not isinstance(networkClientProvider, NetworkClientProvider):
            raise TypeError(f'networkClientProvider argument is malformed: \"{networkClientProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__networkClientProvider: Final[NetworkClientProvider] = networkClientProvider
        self.__timber: Final[TimberInterface] = timber

    async def getSpeech(
        self,
        text: str,
        userKey: str,
        voice: StreamElementsVoice,
    ) -> bytes:
        if not utils.isValidStr(text):
            raise TypeError(f'text argument is malformed: \"{text}\"')
        elif not utils.isValidStr(userKey):
            raise TypeError(f'userKey argument is malformed: \"{userKey}\"')
        elif not isinstance(voice, StreamElementsVoice):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')

        self.__timber.log('StreamElementsApiService', f'Fetching speech... ({voice=}) ({text=})')
        clientSession = await self.__networkClientProvider.get()

        queryString = urllib.parse.urlencode({
            'key': userKey,
            'voice': voice.urlValue,
            'text': text,
        })

        try:
            response = await clientSession.get(
                url = f'https://api.streamelements.com/kappa/v2/speech?{queryString}',
            )
        except GenericNetworkException as e:
            self.__timber.log('StreamElementsApiService', f'Encountered network error when fetching speech ({voice=}) ({text=})', e, traceback.format_exc())
            raise GenericNetworkException(f'StreamElementsApiService encountered network error when fetching speech ({voice=}) ({text=}): {e}')

        responseStatusCode = response.statusCode
        speechBytes = await response.read()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('StreamElementsApiService', f'Encountered non-200 HTTP status code when fetching speech ({voice=}) ({text=}) ({response=}) ({responseStatusCode=})')
            raise GenericNetworkException(
                message = f'StreamElementsApiService encountered non-200 HTTP status code when fetching speech ({voice=}) ({text=}) ({response=}) ({responseStatusCode=})',
                statusCode = responseStatusCode,
            )
        elif speechBytes is None:
            self.__timber.log('StreamElementsApiService', f'Unable to fetch speech bytes ({voice=}) ({text=}) ({response=}) ({responseStatusCode=})')
            raise GenericNetworkException(f'StreamElementsApiService unable to fetch speech bytes ({voice=}) ({text=}) ({response=}) ({responseStatusCode=})')

        return speechBytes
