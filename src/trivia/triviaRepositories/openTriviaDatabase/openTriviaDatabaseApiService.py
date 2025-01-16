import traceback

from .openTriviaDatabaseApiServiceInterface import OpenTriviaDatabaseApiServiceInterface
from .openTriviaDatabaseJsonParserInterface import OpenTriviaDatabaseJsonParserInterface
from .openTriviaDatabaseQuestion import OpenTriviaDatabaseQuestion
from .openTriviaDatabaseResponseCode import OpenTriviaDatabaseResponseCode
from .openTriviaDatabaseSessionToken import OpenTriviaDatabaseSessionToken
from ....misc import utils as utils
from ....network.exceptions import GenericNetworkException
from ....network.networkClientProvider import NetworkClientProvider
from ....network.networkResponse import NetworkResponse
from ....timber.timberInterface import TimberInterface


class OpenTriviaDatabaseApiService(OpenTriviaDatabaseApiServiceInterface):

    def __init__(
        self,
        networkClientProvider: NetworkClientProvider,
        openTriviaDatabaseJsonParser: OpenTriviaDatabaseJsonParserInterface,
        timber: TimberInterface
    ):
        if not isinstance(networkClientProvider, NetworkClientProvider):
            raise TypeError(f'networkClientProvider argument is malformed: \"{networkClientProvider}\"')
        elif not isinstance(openTriviaDatabaseJsonParser, OpenTriviaDatabaseJsonParserInterface):
            raise TypeError(f'openTriviaDatabaseJsonParser argument is malformed: \"{openTriviaDatabaseJsonParser}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__networkClientProvider: NetworkClientProvider = networkClientProvider
        self.__openTriviaDatabaseJsonParser: OpenTriviaDatabaseJsonParserInterface = openTriviaDatabaseJsonParser
        self.__timber: TimberInterface = timber

    async def fetchSessionToken(self) -> OpenTriviaDatabaseSessionToken:
        self.__timber.log('OpenTriviaDatabaseApiService', f'Fetching session token...')
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get('https://opentdb.com/api_token.php?command=request')
        except GenericNetworkException as e:
            self.__timber.log('OpenTriviaDatabaseApiService', f'Encountered network error when fetching session token: {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'OpenTriviaDatabaseApiService encountered network error when fetching session token: {e}')

        responseStatusCode = response.statusCode
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('OpenTriviaDatabaseApiService', f'Encountered non-200 HTTP status code when fetching session token ({responseStatusCode=}) ({response=}) ({jsonResponse=})')
            raise GenericNetworkException(f'OpenTriviaDatabaseApiService encountered non-200 HTTP status code when fetching session token ({responseStatusCode=}) ({response=}) ({jsonResponse=})')

        sessionToken = await self.__openTriviaDatabaseJsonParser.parseSessionToken(jsonResponse)

        if sessionToken is None:
            self.__timber.log('OpenTriviaDatabaseApiService', f'Failed to parse JSON response into OpenTriviaDatabaseSessionToken instance ({responseStatusCode=}) ({response=}) ({jsonResponse=}) ({sessionToken=})')
            raise GenericNetworkException(f'OpenTriviaDatabaseApiService failed to parse JSON response into OpenTriviaDatabaseSessionToken instance ({responseStatusCode=}) ({response=}) ({jsonResponse=}) ({sessionToken=})')

        return sessionToken

    async def fetchTriviaQuestion(
        self,
        sessionToken: str | None,
        twitchChannelId: str
    ) -> OpenTriviaDatabaseQuestion:
        if sessionToken is not None and not isinstance(sessionToken, str):
            raise TypeError(f'sessionToken argument is malformed: \"{sessionToken}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        self.__timber.log('OpenTriviaDatabaseApiService', f'Fetching trivia question...')
        clientSession = await self.__networkClientProvider.get()
        response: NetworkResponse

        try:
            if utils.isValidStr(sessionToken):
                response = await clientSession.get(f'https://opentdb.com/api.php?amount=1&token={sessionToken}')
            else:
                response = await clientSession.get('https://opentdb.com/api.php?amount=1')
        except GenericNetworkException as e:
            self.__timber.log('OpenTriviaDatabaseApiService', f'Encountered network error when fetching trivia question ({sessionToken=}) ({twitchChannelId=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'OpenTriviaDatabaseApiService encountered network error when fetching trivia question ({sessionToken=}) ({twitchChannelId=}): {e}')

        responseStatusCode = response.statusCode
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('OpenTriviaDatabaseApiService', f'Encountered non-200 HTTP status code when fetching trivia question ({responseStatusCode=}) ({response=}) ({jsonResponse=}) ({sessionToken=}) ({twitchChannelId=})')
            raise GenericNetworkException(f'OpenTriviaDatabaseApiService encountered non-200 HTTP status code when fetching trivia question ({responseStatusCode=}) ({response=}) ({jsonResponse=}) ({sessionToken=}) ({twitchChannelId=})')

        questionsResponse = await self.__openTriviaDatabaseJsonParser.parseQuestionsResponse(jsonResponse)

        if questionsResponse is None:
            self.__timber.log('OpenTriviaDatabaseApiService', f'Failed to parse JSON response into OpenTriviaDatabaseQuestionsResponse instance ({responseStatusCode=}) ({response=}) ({jsonResponse=}) ({questionsResponse=}) ({sessionToken=}) ({twitchChannelId=})')
            raise GenericNetworkException(f'OpenTriviaDatabaseApiService failed to parse JSON response into OpenTriviaDatabaseQuestionsResponse instance ({responseStatusCode=}) ({response=}) ({jsonResponse=}) ({questionsResponse=}) ({sessionToken=}) ({twitchChannelId=})')
        elif questionsResponse.responseCode is not OpenTriviaDatabaseResponseCode.SUCCESS:
            self.__timber.log('OpenTriviaDatabaseApiService', f'Encountered bad response code in response data ({responseStatusCode=}) ({response=}) ({jsonResponse=}) ({questionsResponse=}) ({sessionToken=}) ({twitchChannelId=})')
            raise GenericNetworkException(f'OpenTriviaDatabaseApiService encountered bad response code in response data ({responseStatusCode=}) ({response=}) ({jsonResponse=}) ({questionsResponse=}) ({sessionToken=}) ({twitchChannelId=})')
        elif questionsResponse.results is None or len(questionsResponse.results) == 0:
            self.__timber.log('OpenTriviaDatabaseApiService', f'Encountered empty/missing results in response data ({responseStatusCode=}) ({response=}) ({jsonResponse=}) ({questionsResponse=}) ({sessionToken=}) ({twitchChannelId=})')
            raise GenericNetworkException(f'OpenTriviaDatabaseApiService encountered empty/missing results in response data ({responseStatusCode=}) ({response=}) ({jsonResponse=}) ({questionsResponse=}) ({sessionToken=}) ({twitchChannelId=})')

        return questionsResponse.results[0]
