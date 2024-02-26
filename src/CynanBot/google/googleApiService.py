import traceback

import CynanBot.misc.utils as utils
from CynanBot.google.googleApiServiceInterface import GoogleApiServiceInterface
from CynanBot.google.googleJsonMapperInterface import GoogleJsonMapperInterface
from CynanBot.google.googleProjectIdProviderInterface import \
    GoogleProjectIdProviderInterface
from CynanBot.google.googleTranslateTextResponse import \
    GoogleTranslateTextResponse
from CynanBot.google.googleTranslationRequest import GoogleTranslationRequest
from CynanBot.network.exceptions import GenericNetworkException
from CynanBot.network.networkClientProvider import NetworkClientProvider
from CynanBot.timber.timberInterface import TimberInterface


class GoogleApiService(GoogleApiServiceInterface):

    def __init__(
        self,
        googleJsonMapper: GoogleJsonMapperInterface,
        googleProjectIdProvider: GoogleProjectIdProviderInterface,
        networkClientProvider: NetworkClientProvider,
        timber: TimberInterface
    ):
        if not isinstance(googleJsonMapper, GoogleJsonMapperInterface):
            raise TypeError(f'googleJsonMapper argument is malformed: \"{googleJsonMapper}\"')
        elif not isinstance(googleProjectIdProvider, GoogleProjectIdProviderInterface):
            raise TypeError(f'googleProjectIdProvider argument is malformed: \"{googleProjectIdProvider}\"')
        elif not isinstance(networkClientProvider, NetworkClientProvider):
            raise TypeError(f'networkClientProvider argument is malformed: \"{networkClientProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__googleJsonMapper: GoogleJsonMapperInterface = googleJsonMapper
        self.__googleProjectIdProvider: GoogleProjectIdProviderInterface = googleProjectIdProvider
        self.__networkClientProvider: NetworkClientProvider = networkClientProvider
        self.__timber: TimberInterface = timber

    async def translate(self, request: GoogleTranslationRequest) -> GoogleTranslateTextResponse:
        if not isinstance(request, GoogleTranslationRequest):
            raise TypeError(f'request argument is malformed: \"{request}\"')

        self.__timber.log('GoogleApiService', f'Translating... ({request=})')
        clientSession = await self.__networkClientProvider.get()
        projectId = await self.__googleProjectIdProvider.getGoogleProjectId()

        try:
            response = await clientSession.post(
                url = f'https://translate.googleapis.com/v3beta1/{projectId}:translateText'
            )
        except GenericNetworkException as e:
            self.__timber.log('GoogleApiService', f'Encountered network error when fetching translation ({request=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'GoogleApiService encountered network error when fetching traslation ({request=}): {e}')

        if response is None:
            self.__timber.log('GoogleApiService', f'Encountered unknown network error when fetching translation ({request=}) ({response=})')
            raise GenericNetworkException(f'GoogleApiService encountered unknown network error when fetching translation ({request=}) ({response=})')

        responseStatusCode = response.getStatusCode()
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('GoogleApiService', f'Encountered non-200 HTTP status code when fetching translation ({request=}) ({responseStatusCode=}) ({jsonResponse=}) ({response=})')
            raise GenericNetworkException(f'GoogleApiService encountered non-200 HTTP status code when fetching translation ({request=}) ({responseStatusCode=}) ({jsonResponse=}) ({response=})')

        response = await self.__googleJsonMapper.parseTranslateTextResponse(jsonResponse)

        if response is None:
            self.__timber.log('GoogleApiService', f'Failed to parse JSON response into GoogleTranslationRequest instance ({request=}) ({responseStatusCode=}) ({jsonResponse=}) ({response=})')
            raise GenericNetworkException(f'GoogleApiService failed to parse JSON response into GoogleTranslationRequest instance ({request=}) ({responseStatusCode=}) ({jsonResponse=}) ({response=})')

        return response
