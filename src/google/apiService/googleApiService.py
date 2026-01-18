import traceback
from typing import Final

from .googleApiServiceInterface import GoogleApiServiceInterface
from ..accessToken.googleAccessToken import GoogleAccessToken
from ..accessToken.googleApiAccessTokenStorageInterface import GoogleApiAccessTokenStorageInterface
from ..exceptions import GoogleCloudProjectIdUnavailableException
from ..googleCloudProjectCredentialsProviderInterface import GoogleCloudProjectCredentialsProviderInterface
from ..jsonMapper.googleJsonMapperInterface import GoogleJsonMapperInterface
from ..jwtBuilder.googleJwtBuilderInterface import GoogleJwtBuilderInterface
from ..models.googleTextSynthesisResponse import GoogleTextSynthesisResponse
from ..models.googleTextSynthesizeRequest import GoogleTextSynthesizeRequest
from ..models.googleTranslateTextResponse import GoogleTranslateTextResponse
from ..models.googleTranslationRequest import GoogleTranslationRequest
from ...misc import utils as utils
from ...network.exceptions import GenericNetworkException
from ...network.networkClientProvider import NetworkClientProvider
from ...timber.timberInterface import TimberInterface


class GoogleApiService(GoogleApiServiceInterface):

    def __init__(
        self,
        googleApiAccessTokenStorage: GoogleApiAccessTokenStorageInterface,
        googleCloudProjectCredentialsProvider: GoogleCloudProjectCredentialsProviderInterface,
        googleJsonMapper: GoogleJsonMapperInterface,
        googleJwtBuilder: GoogleJwtBuilderInterface,
        networkClientProvider: NetworkClientProvider,
        timber: TimberInterface,
        contentType: str = 'application/json; charset=utf-8',
    ):
        if not isinstance(googleApiAccessTokenStorage, GoogleApiAccessTokenStorageInterface):
            raise TypeError(f'googleApiAccessTokenStorage argument is malformed: \"{googleApiAccessTokenStorage}\"')
        elif not isinstance(googleCloudProjectCredentialsProvider, GoogleCloudProjectCredentialsProviderInterface):
            raise TypeError(f'googleCloudProjectCredentialsProvider argument is malformed: \"{googleCloudProjectCredentialsProvider}\"')
        elif not isinstance(googleJsonMapper, GoogleJsonMapperInterface):
            raise TypeError(f'googleJsonMapper argument is malformed: \"{googleJsonMapper}\"')
        elif not isinstance(googleJwtBuilder, GoogleJwtBuilderInterface):
            raise TypeError(f'googleJwtBuilder argument is malformed: \"{googleJwtBuilder}\"')
        elif not isinstance(networkClientProvider, NetworkClientProvider):
            raise TypeError(f'networkClientProvider argument is malformed: \"{networkClientProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidStr(contentType):
            raise TypeError(f'contentType argument is malformed: \"{contentType}\"')

        self.__googleApiAccessTokenStorage: Final[GoogleApiAccessTokenStorageInterface] = googleApiAccessTokenStorage
        self.__googleCloudProjectCredentialsProvider: Final[GoogleCloudProjectCredentialsProviderInterface] = googleCloudProjectCredentialsProvider
        self.__googleJsonMapper: Final[GoogleJsonMapperInterface] = googleJsonMapper
        self.__googleJwtBuilder: Final[GoogleJwtBuilderInterface] = googleJwtBuilder
        self.__networkClientProvider: Final[NetworkClientProvider] = networkClientProvider
        self.__timber: Final[TimberInterface] = timber
        self.__contentType: Final[str] = contentType

    async def __fetchGoogleAccessToken(self) -> GoogleAccessToken:
        accessToken = await self.__googleApiAccessTokenStorage.getAccessToken()

        if accessToken is not None:
            return accessToken

        self.__timber.log('GoogleApiService', 'Fetching access token from Google...')
        clientSession = await self.__networkClientProvider.get()
        assertion = await self.__googleJwtBuilder.buildJwt()

        try:
            response = await clientSession.post(
                url = 'https://oauth2.googleapis.com/token',
                json = {
                    'assertion': assertion,
                    'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
                },
            )
        except GenericNetworkException as e:
            self.__timber.log('GoogleApiService', f'Encountered network error when fetching access token', e, traceback.format_exc())
            raise GenericNetworkException(f'Encountered network error when fetching access token: {e}')

        responseStatusCode = response.statusCode
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('GoogleApiService', f'Encountered non-200 HTTP status code when fetching access token ({responseStatusCode=}) ({response=}) ({jsonResponse=})')
            raise GenericNetworkException(
                message = f'GoogleApiService encountered non-200 HTTP status code when fetching access token ({responseStatusCode=}) ({response=}) ({jsonResponse=})',
                statusCode = responseStatusCode,
            )

        accessToken = await self.__googleJsonMapper.parseAccessToken(jsonResponse)
        await self.__googleApiAccessTokenStorage.setAccessToken(accessToken)

        if accessToken is None:
            self.__timber.log('GoogleApiService', f'Unable to process server response into access token ({responseStatusCode=}) ({response=}) ({jsonResponse=})')
            raise GenericNetworkException(f'GoogleApiService unable to process server response into access token ({responseStatusCode=}) ({response=}) ({jsonResponse=})')

        return accessToken

    async def __requireGoogleProjectId(self) -> str:
        googleProjectId = await self.__googleCloudProjectCredentialsProvider.getGoogleCloudProjectId()

        if not utils.isValidStr(googleProjectId):
            raise GoogleCloudProjectIdUnavailableException(f'No Google Cloud Project ID is available: \"{googleProjectId}\"')

        return googleProjectId

    async def textToSpeech(self, request: GoogleTextSynthesizeRequest) -> GoogleTextSynthesisResponse:
        if not isinstance(request, GoogleTextSynthesizeRequest):
            raise TypeError(f'request argument is malformed: \"{request}\"')

        self.__timber.log('GoogleApiService', f'Fetching text-to-speech from Google... ({request=})')

        clientSession = await self.__networkClientProvider.get()
        googleProjectId = await self.__requireGoogleProjectId()
        googleAccessToken = await self.__fetchGoogleAccessToken()

        try:
            response = await clientSession.post(
                url = 'https://texttospeech.googleapis.com/v1/text:synthesize',
                headers = {
                    'Accept': self.__contentType,
                    'Authorization': f'Bearer {googleAccessToken.accessToken}',
                    'Content-Type': self.__contentType,
                    'x-goog-user-project': googleProjectId,
                },
                json = await self.__googleJsonMapper.serializeSynthesizeRequest(request),
            )
        except GenericNetworkException as e:
            self.__timber.log('GoogleApiService', f'Encountered network error when fetching text-to-speech ({request=})', e, traceback.format_exc())
            raise GenericNetworkException(f'GoogleApiService encountered network error when fetching text-to-speech ({request=}): {e}')

        responseStatusCode = response.statusCode
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('GoogleApiService', f'Encountered non-200 HTTP status code when fetching text-to-speech ({request=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=})')
            raise GenericNetworkException(
                message = f'GoogleApiService encountered non-200 HTTP status code when fetching text-to-speech ({request=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=})',
                statusCode = responseStatusCode,
            )

        synthesisResponse = await self.__googleJsonMapper.parseTextSynthesisResponse(jsonResponse)

        if synthesisResponse is None:
            self.__timber.log('GoogleApiService', f'Failed to parse JSON response into GoogleTextSynthesizeRequest instance ({request=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=}) ({synthesisResponse=})')
            raise GenericNetworkException(f'GoogleApiService failed to parse JSON response into GoogleTextSynthesizeRequest instance ({request=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=}) ({synthesisResponse=})')

        return synthesisResponse

    async def translate(self, request: GoogleTranslationRequest) -> GoogleTranslateTextResponse:
        if not isinstance(request, GoogleTranslationRequest):
            raise TypeError(f'request argument is malformed: \"{request}\"')

        self.__timber.log('GoogleApiService', f'Fetching translation from Google... ({request=})')

        clientSession = await self.__networkClientProvider.get()
        googleProjectId = await self.__requireGoogleProjectId()
        googleAccessToken = await self.__fetchGoogleAccessToken()

        try:
            response = await clientSession.post(
                url = f'https://translate.googleapis.com/v3/projects/{googleProjectId}:translateText',
                headers = {
                    'Accept': self.__contentType,
                    'Authorization': f'Bearer {googleAccessToken.accessToken}',
                    'Content-Type': self.__contentType,
                    'x-goog-user-project': googleProjectId,
                },
                json = await self.__googleJsonMapper.serializeTranslationRequest(request),
            )
        except GenericNetworkException as e:
            self.__timber.log('GoogleApiService', f'Encountered network error when fetching translation ({request=})', e, traceback.format_exc())
            raise GenericNetworkException(f'GoogleApiService encountered network error when fetching translation ({request=}): {e}')

        responseStatusCode = response.statusCode
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('GoogleApiService', f'Encountered non-200 HTTP status code when fetching translation ({request=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=})')
            raise GenericNetworkException(
                message = f'GoogleApiService encountered non-200 HTTP status code when fetching translation ({request=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=})',
                statusCode = responseStatusCode,
            )

        translateResponse = await self.__googleJsonMapper.parseTranslateTextResponse(jsonResponse)

        if translateResponse is None:
            self.__timber.log('GoogleApiService', f'Failed to parse JSON response into GoogleTranslationRequest instance ({request=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=}) ({translateResponse=})')
            raise GenericNetworkException(f'GoogleApiService failed to parse JSON response into GoogleTranslationRequest instance ({request=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=}) ({translateResponse=})')

        return translateResponse
