import traceback
from typing import Any, Final

from .funtoonApiServiceInterface import FuntoonApiServiceInterface
from ..funtoonTriviaQuestion import FuntoonTriviaQuestion
from ..jsonMapper.funtoonJsonMapperInterface import FuntoonJsonMapperInterface
from ...misc import utils as utils
from ...network.exceptions import GenericNetworkException
from ...network.networkClientProvider import NetworkClientProvider
from ...timber.timberInterface import TimberInterface


class FuntoonApiService(FuntoonApiServiceInterface):

    def __init__(
        self,
        funtoonJsonMapper: FuntoonJsonMapperInterface,
        networkClientProvider: NetworkClientProvider,
        timber: TimberInterface,
    ):
        if not isinstance(funtoonJsonMapper, FuntoonJsonMapperInterface):
            raise TypeError(f'funtoonJsonMapper argument is malformed: \"{funtoonJsonMapper}\"')
        elif not isinstance(networkClientProvider, NetworkClientProvider):
            raise TypeError(f'networkClientProvider argument is malformed: \"{networkClientProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__funtoonJsonMapper: Final[FuntoonJsonMapperInterface] = funtoonJsonMapper
        self.__networkClientProvider: Final[NetworkClientProvider] = networkClientProvider
        self.__timber: Final[TimberInterface] = timber

    async def banTriviaQuestion(self, triviaId: str) -> bool:
        if not utils.isValidStr(triviaId):
            raise TypeError(f'triviaId argument is malformed: \"{triviaId}\"')

        self.__timber.log('FuntoonApiService', f'Banning trivia question ({triviaId=})...')
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get(f'https://funtoon.party/api/trivia/review/{triviaId}')
        except GenericNetworkException as e:
            self.__timber.log('FuntoonApiService', f'Encountered network error when banning trivia question ({triviaId=})', e, traceback.format_exc())
            raise GenericNetworkException(f'FuntoonApiService encountered network error when banning trivia question ({triviaId=}): {e}')

        responseStatusCode = response.statusCode
        await response.close()

        if responseStatusCode == 200:
            self.__timber.log('FuntoonApiService', f'Successfully banned trivia question ({triviaId=}) ({responseStatusCode=})')
            return True
        else:
            self.__timber.log('FuntoonApiService', f'Encountered non-200 HTTP status code when banning trivia question ({triviaId=}) ({responseStatusCode=}) ({response=})')
            return False

    async def customEvent(
        self,
        data: dict[str, Any] | str | None,
        event: str,
        funtoonToken: str,
        twitchChannel: str,
        twitchChannelId: str,
    ) -> bool:
        if data is not None and not isinstance(data, dict) and not isinstance(data, str):
            raise TypeError(f'data argument is malformed: \"{data}\"')
        elif not utils.isValidStr(event):
            raise TypeError(f'event argument is malformed: \"{event}\"')
        elif not utils.isValidStr(funtoonToken):
            raise TypeError(f'funtoonToken argument is malformed: \"{funtoonToken}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        jsonPayload: dict[str, Any] = {
            'channel': twitchChannel,
            'data': data,
            'event': event,
        }

        self.__timber.log('FuntoonApiService', f'Sending custom event... ({data=}) ({event=}) ({funtoonToken=}) ({twitchChannel=}) ({twitchChannelId=}) ({jsonPayload=})')
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.post(
                url = 'https://funtoon.party/api/events/custom',
                headers = {
                    'Authorization': funtoonToken,
                    'Content-Type': 'application/json',
                },
                json = jsonPayload,
            )
        except GenericNetworkException as e:
            self.__timber.log('FuntoonApiService', f'Encountered network error when sending custom event ({data=}) ({event=}) ({funtoonToken=}) ({twitchChannel=}) ({twitchChannelId=}) ({jsonPayload=})', e, traceback.format_exc())
            return False

        responseStatusCode = response.statusCode
        await response.close()

        if responseStatusCode == 200:
            return True
        else:
            self.__timber.log('FuntoonApiService', f'Error sending custom event ({data=}) ({event=}) ({funtoonToken=}) ({twitchChannel=}) ({twitchChannelId=}) ({jsonPayload=}) ({response=}) ({responseStatusCode=})')
            return False

    async def fetchTriviaQuestion(self) -> FuntoonTriviaQuestion:
        self.__timber.log('FuntoonApiService', f'Fetching random trivia question from Funtoon...')
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get('https://funtoon.party/api/trivia/random')
        except GenericNetworkException as e:
            self.__timber.log('FuntoonApiService', f'Encountered network error when fetching random trivia question', e, traceback.format_exc())
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
