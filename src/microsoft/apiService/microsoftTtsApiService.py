import traceback
from typing import Any

from .microsoftTtsApiServiceInterface import MicrosoftTtsApiServiceInterface
from ..models.microsoftTtsVoice import MicrosoftTtsVoice
from ...misc import utils as utils
from ...network.exceptions import GenericNetworkException
from ...network.networkClientProvider import NetworkClientProvider
from ...timber.timberInterface import TimberInterface


class MicrosoftTtsApiService(MicrosoftTtsApiServiceInterface):

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

    async def getSpeech(
        self,
        voice: MicrosoftTtsVoice,
        message: str
    ) -> bytes:
        if not isinstance(voice, MicrosoftTtsVoice):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')
        elif not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')

        self.__timber.log('MicrosoftTtsApiService', f'Fetching speech... ({voice=}) ({message=})')
        clientSession = await self.__networkClientProvider.get()

        json: dict[str, Any] = {
            'message': message,
            'voice': voice.apiValue
        }

        try:
            response = await clientSession.post(
                url = f'http://localhost:9081/sapi/create',
                json = json
            )
        except GenericNetworkException as e:
            self.__timber.log('MicrosoftTtsApiService', f'Encountered network error when fetching speech ({voice=}) ({message=})', e, traceback.format_exc())
            raise GenericNetworkException(f'MicrosoftTtsApiService encountered network error when fetching speech ({voice=}) ({message=}): {e}')

        responseStatusCode = response.statusCode
        speechBytes = await response.read()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('MicrosoftTtsApiService', f'Encountered non-200 HTTP status code when fetching speech ({voice=}) ({message=}) ({response=}) ({responseStatusCode=})')
            raise GenericNetworkException(f'MicrosoftTtsApiService encountered non-200 HTTP status code when fetching speech ({voice=}) ({message=}) ({response=}) ({responseStatusCode=})')
        elif speechBytes is None:
            self.__timber.log('MicrosoftTtsApiService', f'Unable to fetch speech bytes ({voice=}) ({message=}) ({response=}) ({responseStatusCode=})')
            raise GenericNetworkException(f'MicrosoftTtsApiService unable to fetch speech bytes ({voice=}) ({message=}) ({response=}) ({responseStatusCode=})')

        return speechBytes
