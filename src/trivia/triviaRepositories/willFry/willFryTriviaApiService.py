import traceback

from .willFryTriviaApiServiceInterface import WillFryTriviaApiServiceInterface
from .willFryTriviaJsonParserInterface import WillFryTriviaJsonParserInterface
from .willFryTriviaQuestion import WillFryTriviaQuestion
from ....network.exceptions import GenericNetworkException
from ....network.networkClientProvider import NetworkClientProvider
from ....timber.timberInterface import TimberInterface


class WillFryTriviaApiService(WillFryTriviaApiServiceInterface):

    def __init__(
        self,
        networkClientProvider: NetworkClientProvider,
        willFryTriviaJsonParser: WillFryTriviaJsonParserInterface,
        timber: TimberInterface
    ):
        if not isinstance(networkClientProvider, NetworkClientProvider):
            raise TypeError(f'networkClientProvider argument is malformed: \"{networkClientProvider}\"')
        elif not isinstance(willFryTriviaJsonParser, WillFryTriviaJsonParserInterface):
            raise TypeError(f'willFryTriviaJsonParser argument is malformed: \"{willFryTriviaJsonParser}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__networkClientProvider: NetworkClientProvider = networkClientProvider
        self.__willFryTriviaJsonParser: WillFryTriviaJsonParserInterface = willFryTriviaJsonParser
        self.__timber: TimberInterface = timber

    async def fetchTriviaQuestion(self) -> WillFryTriviaQuestion:
        self.__timber.log('WillFryTriviaApiService', 'Fetching trivia question...')
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get('https://the-trivia-api.com/v2/questions?limit=1')
        except GenericNetworkException as e:
            self.__timber.log('WillFryTriviaApiService', f'Encountered network error when fetching trivia question: {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'WillFryTriviaApiService encountered network error when fetching trivia question: {e}')

        responseStatusCode = response.statusCode
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('WillFryTriviaApiService', f'Encountered non-200 HTTP status code when fetching trivia question ({responseStatusCode=}) ({response=}) ({jsonResponse=})')
            raise GenericNetworkException(f'WillFryTriviaApiService encountered non-200 HTTP status code when fetching trivia question ({responseStatusCode=}) ({response=}) ({jsonResponse=})')

        triviaQuestions = await self.__willFryTriviaJsonParser.parseTriviaQuestions(jsonResponse)

        if triviaQuestions is None or len(triviaQuestions) == 0:
            self.__timber.log('WillFryTriviaApiService', f'Failed to parse JSON response into WillFryTriviaQuestion list ({responseStatusCode=}) ({response=}) ({jsonResponse=}) ({triviaQuestions=})')
            raise GenericNetworkException(f'WillFryTriviaApiService failed to parse JSON response into WillFryTriviaQuestion list ({responseStatusCode=}) ({response=}) ({jsonResponse=}) ({triviaQuestions=})')

        return triviaQuestions[0]
