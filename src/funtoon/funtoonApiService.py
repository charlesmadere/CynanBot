import traceback

from .funtoonApiServiceInterface import FuntoonApiServiceInterface
from .funtoonJsonMapperInterface import FuntoonJsonMapperInterface
from .funtoonTriviaQuestion import FuntoonTriviaQuestion
from ..misc import utils as utils
from ..network.exceptions import GenericNetworkException
from ..network.networkClientProvider import NetworkClientProvider
from ..timber.timberInterface import TimberInterface


class FuntoonApiService(FuntoonApiServiceInterface):

    def __init__(
        self,
        funtoonJsonMapper: FuntoonJsonMapperInterface,
        networkClientProvider: NetworkClientProvider,
        timber: TimberInterface
    ):
        if not isinstance(funtoonJsonMapper, FuntoonJsonMapperInterface):
            raise TypeError(f'funtoonJsonMapper argument is malformed: \"{funtoonJsonMapper}\"')
        elif not isinstance(networkClientProvider, NetworkClientProvider):
            raise TypeError(f'networkClientProvider argument is malformed: \"{networkClientProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__funtoonJsonMapper: FuntoonJsonMapperInterface = funtoonJsonMapper
        self.__networkClientProvider: NetworkClientProvider = networkClientProvider
        self.__timber: TimberInterface = timber

    async def banTriviaQuestion(self, triviaId: str) -> bool:
        if not utils.isValidStr(triviaId):
            raise TypeError(f'triviaId argument is malformed: \"{triviaId}\"')

        self.__timber.log('FuntoonApiService', f'Banning trivia question ({triviaId=})...')
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get(f'https://funtoon.party/api/trivia/review/{triviaId}')
        except GenericNetworkException as e:
            self.__timber.log('FuntoonApiService', f'Encountered network error when banning trivia question ({triviaId=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'FuntoonApiService encountered network error when banning trivia question ({triviaId=}): {e}')

        responseStatusCode = response.statusCode
        await response.close()

        if responseStatusCode == 200:
            self.__timber.log('FuntoonApiService', f'Successfully banned trivia question ({triviaId=}) ({responseStatusCode=})')
            return True
        else:
            self.__timber.log('FuntoonApiService', f'Encountered non-200 HTTP status code when banning trivia question ({triviaId=}) ({responseStatusCode=}) ({response=})')
            return False

    async def fetchTriviaQuestion(self) -> FuntoonTriviaQuestion:
        self.__timber.log('FuntoonApiService', f'Fetching random trivia question from Funtoon...')
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get('https://funtoon.party/api/trivia/random')
        except GenericNetworkException as e:
            self.__timber.log('FuntoonApiService', f'Encountered network error when fetching random trivia question: {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'FuntoonApiService encountered network error when fetching random trivia question: {e}')

        responseStatusCode = response.statusCode
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('FuntoonApiService', f'Encountered non-200 HTTP status code when fetching random trivia question ({responseStatusCode=}) ({response=}) ({jsonResponse=})')
            raise GenericNetworkException(f'FuntoonApiService encountered non-200 HTTP status code when fetching random trivia question ({responseStatusCode=}) ({response=}) ({jsonResponse=})')

        triviaQuestion = await self.__funtoonJsonMapper.parseTriviaQuestion(jsonResponse)

        if triviaQuestion is None:
            self.__timber.log('FuntoonApiService', f'Failed to parse JSON response into FuntoonTriviaQuestion instance ({responseStatusCode=}) ({response=}) ({jsonResponse=}) ({triviaQuestion=})')
            raise GenericNetworkException(f'FuntoonApiService failed to parse JSON response into FuntoonTriviaQuestion instance ({responseStatusCode=}) ({response=}) ({jsonResponse=}) ({triviaQuestion=})')

        return triviaQuestion
