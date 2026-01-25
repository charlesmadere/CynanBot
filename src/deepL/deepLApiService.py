import traceback
from typing import Final

from .deepLApiServiceInterface import DeepLApiServiceInterface
from .deepLAuthKeyProviderInterface import DeepLAuthKeyProviderInterface
from .deepLJsonMapperInterface import DeepLJsonMapperInterface
from .deepLTranslationRequest import DeepLTranslationRequest
from .deepLTranslationResponses import DeepLTranslationResponses
from .exceptions import DeepLAuthKeyUnavailableException
from ..misc import utils as utils
from ..network.exceptions import GenericNetworkException
from ..network.networkClientProvider import NetworkClientProvider
from ..timber.timberInterface import TimberInterface


class DeepLApiService(DeepLApiServiceInterface):

    def __init__(
        self,
        deepLAuthKeyProvider: DeepLAuthKeyProviderInterface,
        deepLJsonMapper: DeepLJsonMapperInterface,
        networkClientProvider: NetworkClientProvider,
        timber: TimberInterface,
        contentType: str = 'application/json',
    ):
        if not isinstance(deepLAuthKeyProvider, DeepLAuthKeyProviderInterface):
            raise TypeError(f'deepLAuthKeyProviderInterface argument is malformed: \"{deepLAuthKeyProvider}\"')
        elif not isinstance(deepLJsonMapper, DeepLJsonMapperInterface):
            raise TypeError(f'deepLJsonMapper argument is malformed: \"{deepLJsonMapper}\"')
        elif not isinstance(networkClientProvider, NetworkClientProvider):
            raise TypeError(f'networkClientProvider argument is malformed: \"{networkClientProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidStr(contentType):
            raise TypeError(f'contentType argument is malformed: \"{contentType}\"')

        self.__deepLAuthKeyProvider: Final[DeepLAuthKeyProviderInterface] = deepLAuthKeyProvider
        self.__deepLJsonMapper: Final[DeepLJsonMapperInterface] = deepLJsonMapper
        self.__networkClientProvider: Final[NetworkClientProvider] = networkClientProvider
        self.__timber: Final[TimberInterface] = timber
        self.__contentType: Final[str] = contentType

    async def translate(
        self,
        request: DeepLTranslationRequest,
    ) -> DeepLTranslationResponses:
        if not isinstance(request, DeepLTranslationRequest):
            raise TypeError(f'request argument is malformed: \"{request}\"')

        self.__timber.log('DeepLApiService', f'Fetching translation from DeepL... ({request=})')
        clientSession = await self.__networkClientProvider.get()

        deepLAuthKey = await self.__deepLAuthKeyProvider.getDeepLAuthKey()
        if not utils.isValidStr(deepLAuthKey):
            raise DeepLAuthKeyUnavailableException(f'No DeepL authentication key is available: \"{deepLAuthKey}\"')

        try:
            response = await clientSession.post(
                url = 'https://api-free.deepl.com/v2/translate',
                headers = {
                    'Authorization': f'DeepL-Auth-Key {deepLAuthKey}',
                    'Content-Type': self.__contentType,
                },
                json = await self.__deepLJsonMapper.serializeTranslationRequest(request),
            )
        except GenericNetworkException as e:
            self.__timber.log('DeepLApiService', f'Encountered network error when fetching translation ({request=})', e, traceback.format_exc())
            raise GenericNetworkException(f'DeepLApiService encountered network error when fetching translation ({request=}): {e}')

        responseStatusCode = response.statusCode
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('DeepLApiService', f'Encountered non-200 HTTP status code when fetching translation ({request=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=})')
            raise GenericNetworkException(
                message = f'DeepLApiService encountered non-200 HTTP status code when fetching translation ({request=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=})',
                statusCode = responseStatusCode,
            )

        translationResponses = await self.__deepLJsonMapper.parseTranslationResponses(jsonResponse)

        if translationResponses is None:
            self.__timber.log('DeepLApiService', f'Failed to parse JSON response into DeepLTranslationResponses instance ({request=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=}) ({translationResponses=})')
            raise GenericNetworkException(f'DeepLApiService failed to parse JSON response into DeepLTranslationResponses instance ({request=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=}) ({translationResponses=})')

        return translationResponses
