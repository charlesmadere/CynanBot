from .ttsMonsterPrivateApiServiceInterface import TtsMonsterPrivateApiServiceInterface
from ..mapper.ttsMonsterPrivateApiJsonMapperInterface import TtsMonsterPrivateApiJsonMapperInterface
from ..models.ttsMonsterPrivateApiTtsResponse import TtsMonsterPrivateApiTtsResponse
from ...network.exceptions import GenericNetworkException
from ...network.networkClientProvider import NetworkClientProvider
from ...timber.timberInterface import TimberInterface


class TtsMonsterPrivateApiService(TtsMonsterPrivateApiServiceInterface):

    def __init__(
        self,
        networkClientProvider: NetworkClientProvider,
        timber: TimberInterface,
        ttsMonsterPrivateApiJsonMapper: TtsMonsterPrivateApiJsonMapperInterface,
        provider: str = 'provider'
    ):
        if not isinstance(networkClientProvider, NetworkClientProvider):
            raise TypeError(f'networkClientProvider argument is malformed: \"{networkClientProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsMonsterPrivateApiJsonMapper, TtsMonsterPrivateApiJsonMapperInterface):
            raise TypeError(f'ttsMonsterPrivateApiJsonMapper argument is malformed: \"{ttsMonsterPrivateApiJsonMapper}\"')
        elif not utils.isValidStr(provider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__networkClientProvider: NetworkClientProvider = networkClientProvider
        self.__timber: TimberInterface = timber
        self.__ttsMonsterPrivateApiJsonMapper: TtsMonsterPrivateApiJsonMapperInterface = ttsMonsterPrivateApiJsonMapper
        self.__provider: str = provider

    async def generateTts(
        self,
        key: str,
        message: str,
        userId: str
    ) -> TtsMonsterPrivateApiTtsResponse:
        if not utils.isValidStr(key):
            raise TypeError(f'key argument is malformed: \"{key}\"')
        elif not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{apiToken}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        self.__timber.log('TtsMonsterApiService', f'Generating TTS using private API... ({key=}) ({message=}) ({userId=})')
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.post(
                url = f'https://us-central1-tts-monster.cloudfunctions.net/generateTTS',
                json = {
                    'data': {
                        'ai': True,
                        'details': {
                            'provider': self.__provider
                        },
                        'key': key,
                        'message': message,
                        'userId': userId
                    }
                }
            )
        except GenericNetworkException as e:
            self.__timber.log('TtsMonsterPrivateApiService', f'Encountered network error when generating TTS ({key=}) ({message=}) ({userId=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'TtsMonsterPrivateApiService encountered network error when generating TTS ({key=}) ({message=}) ({userId=}): {e}')

        responseStatusCode = response.statusCode
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('TtsMonsterPrivateApiService', f'Encountered non-200 HTTP status code when generating TTS ({key=}) ({message=}) ({userId=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise GenericNetworkException(f'TtsMonsterPrivateApiService encountered non-200 HTTP status code when generating TTS ({key=}) ({message=}) ({userId=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})', responseStatusCode)

        privateApiTtsResponse = await self.__ttsMonsterPrivateApiJsonMapper.parseTtsResponse(jsonResponse)

        if privateApiTtsResponse is None:
            self.__timber.log('TtsMonsterApiService', f'Unable to parse JSON response when generating TTS ({key=}) ({message=}) ({userId=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({privateApiTtsResponse=})')
            raise GenericNetworkException(f'TtsMonsterApiService unable to parse JSON response when generating TTS ({key=}) ({message=}) ({userId=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({privateApiTtsResponse=})')

        return privateApiTtsResponse
