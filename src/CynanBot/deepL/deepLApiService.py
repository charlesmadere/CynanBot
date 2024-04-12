import traceback

from CynanBot.deepL.deepLJsonMapperInterface import DeepLJsonMapperInterface
from CynanBot.deepL.deepLTranslationRequest import DeepLTranslationRequest
from CynanBot.deepL.exceptions import DeepLAuthKeyUnavailableException
import CynanBot.misc.utils as utils
from CynanBot.deepL.deepLAuthKeyProviderInterface import DeepLAuthKeyProviderInterface
from CynanBot.deepL.deepLApiServiceInterface import DeepLApiServiceInterface
from CynanBot.deepL.deepLTranslationResponses import DeepLTranslationResponses
from CynanBot.network.exceptions import GenericNetworkException
from CynanBot.network.networkClientProvider import NetworkClientProvider
from CynanBot.timber.timberInterface import TimberInterface


class DeepLApiService(DeepLApiServiceInterface):

    def __init__(
        self,
        deepLAuthKeyProvider: DeepLAuthKeyProviderInterface,
        deepLJsonMapper: DeepLJsonMapperInterface,
        networkClientProvider: NetworkClientProvider,
        timber: TimberInterface,
        contentType: str = 'application/json'
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

        self.__deepLAuthKeyProvider: DeepLAuthKeyProviderInterface = deepLAuthKeyProvider
        self.__deepLJsonMapper: DeepLJsonMapperInterface = deepLJsonMapper
        self.__networkClientProvider: NetworkClientProvider = networkClientProvider
        self.__timber: TimberInterface = timber
        self.__contentType: str = contentType

    async def translate(
        self,
        request: DeepLTranslationRequest
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
                url = f'https://api-free.deepl.com/v2/translate',
                headers = {
                    'Authorization': f'DeepL-Auth-Key {deepLAuthKey}',
                    'Content-Type': self.__contentType
                },
                json = await self.__deepLJsonMapper.serializeTranslationRequest(request)
            )
        except GenericNetworkException as e:
            self.__timber.log('DeepLApiService', f'Encountered network error when fetching translation ({request=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'DeepLApiService encountered network error when fetching translation ({request=}): {e}')

        if response is None:
            self.__timber.log('DeepLApiService', f'Encountered unknown network error when fetching translation ({request=}) ({response=})')
            raise GenericNetworkException(f'DeepLApiService encountered unknown network error when fetching translation ({request=}) ({response=})')

        responseStatusCode = response.getStatusCode()
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('DeepLApiService', f'Encountered non-200 HTTP status code when fetching translation ({request=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=})')
            raise GenericNetworkException(f'DeepLApiService encountered non-200 HTTP status code when fetching translation ({request=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=})')

        translationResponses = await self.__deepLJsonMapper.parseTranslationResponses(jsonResponse)

        if translationResponses is None:
            self.__timber.log('DeepLApiService', f'Failed to parse JSON response into DeepLTranslationResponses instance ({request=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=}) ({translationResponses=})')
            raise GenericNetworkException(f'DeepLApiService failed to parse JSON response into DeepLTranslationResponses instance ({request=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=}) ({translationResponses=})')

        return translationResponses
