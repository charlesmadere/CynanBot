import traceback
from typing import Final

from .ttsMonsterPrivateApiServiceInterface import TtsMonsterPrivateApiServiceInterface
from ..mapper.ttsMonsterPrivateApiJsonMapperInterface import TtsMonsterPrivateApiJsonMapperInterface
from ..models.ttsMonsterPrivateApiTtsResponse import TtsMonsterPrivateApiTtsResponse
from ...misc import utils as utils
from ...network.exceptions import GenericNetworkException
from ...network.networkClientProvider import NetworkClientProvider
from ...timber.timberInterface import TimberInterface


class TtsMonsterPrivateApiService(TtsMonsterPrivateApiServiceInterface):

    def __init__(
        self,
        networkClientProvider: NetworkClientProvider,
        timber: TimberInterface,
        ttsMonsterPrivateApiJsonMapper: TtsMonsterPrivateApiJsonMapperInterface
    ):
        if not isinstance(networkClientProvider, NetworkClientProvider):
            raise TypeError(f'networkClientProvider argument is malformed: \"{networkClientProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsMonsterPrivateApiJsonMapper, TtsMonsterPrivateApiJsonMapperInterface):
            raise TypeError(f'ttsMonsterPrivateApiJsonMapper argument is malformed: \"{ttsMonsterPrivateApiJsonMapper}\"')

        self.__networkClientProvider: Final[NetworkClientProvider] = networkClientProvider
        self.__timber: Final[TimberInterface] = timber
        self.__ttsMonsterPrivateApiJsonMapper: Final[TtsMonsterPrivateApiJsonMapperInterface] = ttsMonsterPrivateApiJsonMapper

    async def fetchGeneratedTts(
        self,
        ttsUrl: str
    ) -> bytes:
        if not utils.isValidUrl(ttsUrl):
            raise TypeError(f'ttsUrl argument is malformed: \"{ttsUrl}\"')

        self.__timber.log('TtsMonsterPrivateApiService', f'Fetching generated TTS...')
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get(url = ttsUrl)
        except GenericNetworkException as e:
            self.__timber.log('TtsMonsterPrivateApiService', f'Encountered network error when fetching generated TTS ({ttsUrl=})', e, traceback.format_exc())
            raise GenericNetworkException(f'TtsMonsterPrivateApiService encountered network error when fetching generated TTS ({ttsUrl=}): {e}')

        responseStatusCode = response.statusCode
        speechBytes = await response.read()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('TtsMonsterPrivateApiService', f'Encountered non-200 HTTP status code when generating TTS ({ttsUrl=}) ({response=}) ({responseStatusCode=})')
            raise GenericNetworkException(f'TtsMonsterPrivateApiService encountered non-200 HTTP status code when generating TTS ({ttsUrl=}) ({response=}) ({responseStatusCode=})', responseStatusCode)
        elif speechBytes is None:
            self.__timber.log('TtsMonsterPrivateApiService', f'Unable to fetch generated TTS bytes ({ttsUrl=}) ({response=}) ({responseStatusCode=})')
            raise GenericNetworkException(f'TtsMonsterPrivateApiService unable to fetch generated TTS bytes ({ttsUrl=}) ({response=}) ({responseStatusCode=})')

        return speechBytes

    async def generateTts(
        self,
        key: str,
        message: str,
        userId: str
    ) -> TtsMonsterPrivateApiTtsResponse:
        if not utils.isValidStr(key):
            raise TypeError(f'key argument is malformed: \"{key}\"')
        elif not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        self.__timber.log('TtsMonsterPrivateApiService', f'Generating TTS... ({key=}) ({message=}) ({userId=})')
        clientSession = await self.__networkClientProvider.get()

        jsonBody = await self.__ttsMonsterPrivateApiJsonMapper.serializeGenerateTtsJsonBody(
            key = key,
            message = message,
            userId = userId,
        )

        try:
            response = await clientSession.post(
                url = f'https://us-central1-tts-monster.cloudfunctions.net/generateTTS',
                json = jsonBody,
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
            self.__timber.log('TtsMonsterPrivateApiService', f'Unable to parse JSON response when generating TTS ({key=}) ({message=}) ({userId=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({privateApiTtsResponse=})')
            raise GenericNetworkException(f'TtsMonsterPrivateApiService unable to parse JSON response when generating TTS ({key=}) ({message=}) ({userId=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({privateApiTtsResponse=})')

        return privateApiTtsResponse
