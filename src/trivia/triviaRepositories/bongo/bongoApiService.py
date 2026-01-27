import traceback
from typing import Final

from .bongoApiServiceInterface import BongoApiServiceInterface
from .bongoJsonParserInterface import BongoJsonParserInterface
from .bongoTriviaQuestion import BongoTriviaQuestion
from ....network.exceptions import GenericNetworkException
from ....network.networkClientProvider import NetworkClientProvider
from ....timber.timberInterface import TimberInterface


class BongoApiService(BongoApiServiceInterface):

    def __init__(
        self,
        bongoJsonParser: BongoJsonParserInterface,
        networkClientProvider: NetworkClientProvider,
        timber: TimberInterface,
    ):
        if not isinstance(bongoJsonParser, BongoJsonParserInterface):
            raise TypeError(f'bongoJsonParser argument is malformed: \"{bongoJsonParser}\"')
        elif not isinstance(networkClientProvider, NetworkClientProvider):
            raise TypeError(f'networkClientProvider argument is malformed: \"{networkClientProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__bongoJsonParser: Final[BongoJsonParserInterface] = bongoJsonParser
        self.__networkClientProvider: Final[NetworkClientProvider] = networkClientProvider
        self.__timber: Final[TimberInterface] = timber

    async def fetchTriviaQuestion(self) -> BongoTriviaQuestion:
        self.__timber.log('BongoApiService', f'Fetching trivia question...')
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get('https://beta-trivia.bongo.best/?limit=1')
        except GenericNetworkException as e:
            self.__timber.log('BongoApiService', f'Encountered network error when fetching trivia question', e, traceback.format_exc())
            raise GenericNetworkException(f'BongoApiService encountered network error when fetching trivia question: {e}')

        responseStatusCode = response.statusCode
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('BongoApiService', f'Encountered non-200 HTTP status code when fetching trivia question ({responseStatusCode=}) ({response=}) ({jsonResponse=})')
            raise GenericNetworkException(
                message = f'BongoApiService encountered non-200 HTTP status code when fetching trivia question ({responseStatusCode=}) ({response=}) ({jsonResponse=})',
                statusCode = responseStatusCode,
            )

        questions = await self.__bongoJsonParser.parseTriviaQuestions(jsonResponse)

        if questions is None or len(questions) == 0:
            self.__timber.log('BongoApiService', f'Failed to parse JSON response into any BongoTriviaQuestion instance ({responseStatusCode=}) ({response=}) ({jsonResponse=}) ({questions=})')
            raise GenericNetworkException(f'BongoApiService failed to parse JSON response into any BongoTriviaQuestion instance ({responseStatusCode=}) ({response=}) ({jsonResponse=}) ({questions=})')

        return questions[0]
