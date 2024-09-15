import traceback

from .ttsMonsterApiServiceInterface import TtsMonsterApiServiceInterface
from ..mapper.ttsMonsterJsonMapperInterface import TtsMonsterJsonMapperInterface
from ..models.ttsMonsterTtsRequest import TtsMonsterTtsRequest
from ..models.ttsMonsterTtsResponse import TtsMonsterTtsResponse
from ..models.ttsMonsterUser import TtsMonsterUser
from ..models.ttsMonsterVoicesResponse import TtsMonsterVoicesResponse
from ...misc import utils as utils
from ...network.exceptions import GenericNetworkException
from ...network.networkClientProvider import NetworkClientProvider
from ...timber.timberInterface import TimberInterface


class TtsMonsterApiService(TtsMonsterApiServiceInterface):

    def __init__(
        self,
        networkClientProvider: NetworkClientProvider,
        timber: TimberInterface,
        ttsMonsterJsonMapper: TtsMonsterJsonMapperInterface,
        contentType: str = 'application/json'
    ):
        if not isinstance(networkClientProvider, NetworkClientProvider):
            raise TypeError(f'networkClientProvider argument is malformed: \"{networkClientProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsMonsterJsonMapper, TtsMonsterJsonMapperInterface):
            raise TypeError(f'ttsMonsterJsonMapper argument is malformed: \"{ttsMonsterJsonMapper}\"')
        elif not utils.isValidStr(contentType):
            raise TypeError(f'contentType argument is malformed: \"{contentType}\"')

        self.__networkClientProvider: NetworkClientProvider = networkClientProvider
        self.__timber: TimberInterface = timber
        self.__ttsMonsterJsonMapper: TtsMonsterJsonMapperInterface = ttsMonsterJsonMapper
        self.__contentType: str = contentType

    async def fetchGeneratedTts(self, ttsUrl: str) -> bytes:
        if not utils.isValidUrl(ttsUrl):
            raise TypeError(f'ttsUrl argument is malformed: \"{ttsUrl}\"')

        self.__timber.log('TtsMonsterApiService', f'Fetching generated TTS... ({ttsUrl=})')
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get(url = ttsUrl)
        except GenericNetworkException as e:
            self.__timber.log('TtsMonsterApiService', f'Encountered network error when fetching generated TTS ({ttsUrl=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'TtsMonsterApiService encountered network error when fetching generated TTS ({ttsUrl=}): {e}')

        responseStatusCode = response.statusCode
        generatedTtsBytes = await response.read()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('TtsMonsterApiService', f'Encountered non-200 HTTP status code when generating TTS ({ttsUrl=}) ({response=}) ({responseStatusCode=})')
            raise GenericNetworkException(f'TtsMonsterApiService encountered non-200 HTTP status code when generating TTS ({ttsUrl=}) ({response=}) ({responseStatusCode=})', responseStatusCode)

        return generatedTtsBytes

    async def generateTts(
        self,
        apiToken: str,
        request: TtsMonsterTtsRequest
    ) -> TtsMonsterTtsResponse:
        if not utils.isValidStr(apiToken):
            raise TypeError(f'apiToken argument is malformed: \"{apiToken}\"')
        elif not isinstance(request, TtsMonsterTtsRequest):
            raise TypeError(f'request argument is malformed: \"{request}\"')

        self.__timber.log('TtsMonsterApiService', f'Generating TTS... ({apiToken=}) ({request=})')
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.post(
                url = 'https://api.console.tts.monster/generate',
                headers = {
                    'Authorization': apiToken,
                    'Content-Type': self.__contentType
                },
                json = await self.__ttsMonsterJsonMapper.serializeTtsRequest(request)
            )
        except GenericNetworkException as e:
            self.__timber.log('TtsMonsterApiService', f'Encountered network error when generating TTS ({apiToken=}) ({request=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'TtsMonsterApiService encountered network error when generating TTS ({apiToken=}) ({request=}): {e}')

        responseStatusCode = response.statusCode
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('TtsMonsterApiService', f'Encountered non-200 HTTP status code when generating TTS ({apiToken=}) ({request=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise GenericNetworkException(f'TtsMonsterApiService encountered non-200 HTTP status code when generating TTS ({apiToken=}) ({request=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})', responseStatusCode)

        ttsMonsterTtsResponse = await self.__ttsMonsterJsonMapper.parseTtsResponse(jsonResponse)

        if ttsMonsterTtsResponse is None:
            self.__timber.log('TtsMonsterApiService', f'Unable to parse JSON response when generating TTS ({apiToken=}) ({request=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({ttsMonsterTtsResponse=})')
            raise GenericNetworkException(f'TtsMonsterApiService unable to parse JSON response when generating TTS ({apiToken=}) ({request=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({ttsMonsterTtsResponse=})')
        elif ttsMonsterTtsResponse.status != 200:
            self.__timber.log('TtsMonsterApiService', f'Generated TTS but the API service responded with a bad \"status\" value in its JSON response ({apiToken=}) ({request=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({ttsMonsterTtsResponse=})')
            raise GenericNetworkException(f'TtsMonsterApiService generated TTS but the API service responded with a bad \"status\" value in its JSON response ({apiToken=}) ({request=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({ttsMonsterTtsResponse=})')

        return ttsMonsterTtsResponse

    async def getUser(self, apiToken: str) -> TtsMonsterUser:
        if not utils.isValidStr(apiToken):
            raise TypeError(f'apiToken argument is malformed: \"{apiToken}\"')

        self.__timber.log('TtsMonsterApiService', f'Getting user... ({apiToken=})')
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.post(
                url = 'https://api.console.tts.monster/user',
                headers = {
                    'Authorization': apiToken,
                }
            )
        except GenericNetworkException as e:
            self.__timber.log('TtsMonsterApiService', f'Encountered network error when getting user ({apiToken=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'TtsMonsterApiService encountered network error when getting user ({apiToken=}): {e}')

        responseStatusCode = response.statusCode
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('TtsMonsterApiService', f'Encountered non-200 HTTP status code when getting user ({apiToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise GenericNetworkException(f'TtsMonsterApiService encountered non-200 HTTP status code when getting user ({apiToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})', responseStatusCode)

        user = await self.__ttsMonsterJsonMapper.parseUser(jsonResponse)

        if user is None:
            self.__timber.log('TtsMonsterApiService', f'Unable to parse JSON response when getting user ({apiToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({user=})')
            raise GenericNetworkException(f'TtsMonsterApiService unable to parse JSON response when getting user ({apiToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({user=})')

        return user

    async def getVoices(self, apiToken: str) -> TtsMonsterVoicesResponse:
        if not utils.isValidStr(apiToken):
            raise TypeError(f'apiToken argument is malformed: \"{apiToken}\"')

        self.__timber.log('TtsMonsterApiService', f'Getting voices... ({apiToken=})')
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.post(
                url = 'https://api.console.tts.monster/voices',
                headers = {
                    'Authorization': apiToken,
                }
            )
        except GenericNetworkException as e:
            self.__timber.log('TtsMonsterApiService', f'Encountered network error when getting voices ({apiToken=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'TtsMonsterApiService encountered network error when getting voices ({apiToken=}): {e}')

        responseStatusCode = response.statusCode
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('TtsMonsterApiService', f'Encountered non-200 HTTP status code when getting voices ({apiToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise GenericNetworkException(f'TtsMonsterApiService encountered non-200 HTTP status code when getting voices ({apiToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})', responseStatusCode)

        voicesResponse = await self.__ttsMonsterJsonMapper.parseVoicesResponse(jsonResponse)

        if voicesResponse is None:
            self.__timber.log('TtsMonsterApiService', f'Unable to parse JSON response when getting voices ({apiToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({voicesResponse=})')
            raise GenericNetworkException(f'TtsMonsterApiService unable to parse JSON response when getting voices ({apiToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({voicesResponse=})')
        elif (voicesResponse.voices is None or len(voicesResponse.voices) == 0) and (voicesResponse.customVoices is None or len(voicesResponse.customVoices) == 0):
            self.__timber.log('TtsMonsterApiService', f'Received empty voices response when getting voices ({apiToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({voicesResponse=})')
            raise GenericNetworkException(f'TtsMonsterApiService received empty voices response when getting voices ({apiToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({voicesResponse=})')

        return voicesResponse
