import traceback
import urllib.parse
from typing import Final

from .microsoftSamApiServiceInterface import MicrosoftSamApiServiceInterface
from ..models.microsoftSamVoice import MicrosoftSamVoice
from ...misc import utils as utils
from ...network.exceptions import GenericNetworkException
from ...network.networkClientProvider import NetworkClientProvider
from ...timber.timberInterface import TimberInterface


class MicrosoftSamApiService(MicrosoftSamApiServiceInterface):

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
        voice: MicrosoftSamVoice,
        text: str,
    ) -> bytes:
        if not isinstance(voice, MicrosoftSamVoice):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')
        elif not utils.isValidStr(text):
            raise TypeError(f'text argument is malformed: \"{text}\"')

        self.__timber.log('MicrosoftSamApiService', f'Fetching speech... ({voice=}) ({text=})')
        clientSession = await self.__networkClientProvider.get()

        queryString = urllib.parse.urlencode({
            'pitch': voice.pitch,
            'speed': voice.speed,
            'text': text,
            'voice': voice.apiValue,
        })

        try:
            response = await clientSession.get(
                url = f'https://www.tetyys.com/SAPI4/SAPI4?{queryString}',
            )
        except GenericNetworkException as e:
            self.__timber.log('MicrosoftSamApiService', f'Encountered network error when fetching speech ({voice=}) ({text=})', e, traceback.format_exc())
            raise GenericNetworkException(f'MicrosoftSamApiService encountered network error when fetching speech ({voice=}) ({text=}): {e}')

        responseStatusCode = response.statusCode
        speechBytes = await response.read()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('MicrosoftSamApiService', f'Encountered non-200 HTTP status code when fetching speech ({voice=}) ({text=}) ({response=}) ({responseStatusCode=})')
            raise GenericNetworkException(
                message = f'MicrosoftSamApiService encountered non-200 HTTP status code when fetching speech ({voice=}) ({text=}) ({response=}) ({responseStatusCode=})',
                statusCode = responseStatusCode,
            )
        elif speechBytes is None:
            self.__timber.log('MicrosoftSamApiService', f'Unable to fetch speech bytes ({voice=}) ({text=}) ({response=}) ({responseStatusCode=})')
            raise GenericNetworkException(f'MicrosoftSamApiService unable to fetch speech bytes ({voice=}) ({text=}) ({response=}) ({responseStatusCode=})')

        return speechBytes
