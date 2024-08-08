import traceback

from .openTriviaDatabaseApiServiceInterface import OpenTriviaDatabaseApiServiceInterface
from .openTriviaDatabaseQuestion import OpenTriviaDatabaseQuestion
from .openTriviaDatabaseQuestionFetcherInterface import OpenTriviaDatabaseQuestionFetcherInterface
from .openTriviaDatabaseSessionTokenRepositoryInterface import OpenTriviaDatabaseSessionTokenRepositoryInterface
from ....misc import utils as utils
from ....network.exceptions import GenericNetworkException
from ....timber.timberInterface import TimberInterface


class OpenTriviaDatabaseQuestionFetcher(OpenTriviaDatabaseQuestionFetcherInterface):

    def __init__(
        self,
        openTriviaDatabaseApiService: OpenTriviaDatabaseApiServiceInterface,
        openTriviaDatabaseSessionTokenRepository: OpenTriviaDatabaseSessionTokenRepositoryInterface,
        timber: TimberInterface
    ):
        if not isinstance(openTriviaDatabaseApiService, OpenTriviaDatabaseApiServiceInterface):
            raise TypeError(f'openTriviaDatabaseApiService argument is malformed: \"{openTriviaDatabaseApiService}\"')
        elif not isinstance(openTriviaDatabaseSessionTokenRepository, OpenTriviaDatabaseSessionTokenRepositoryInterface):
            raise TypeError(f'openTriviaDatabaseSessionTokenRepository argument is malformed: \"{openTriviaDatabaseSessionTokenRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__openTriviaDatabaseApiService: OpenTriviaDatabaseApiServiceInterface = openTriviaDatabaseApiService
        self.__openTriviaDatabaseSessionTokenRepository: OpenTriviaDatabaseSessionTokenRepositoryInterface = openTriviaDatabaseSessionTokenRepository
        self.__timber: TimberInterface = timber

    async def fetchTriviaQuestion(self, twitchChannelId: str) -> OpenTriviaDatabaseQuestion:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        attempt = 0
        maxAttempts = 2
        sessionTokenString = await self.__openTriviaDatabaseSessionTokenRepository.get(twitchChannelId)

        while attempt < maxAttempts:
            if not utils.isValidStr(sessionTokenString) or attempt == 1:
                sessionToken = await self.__openTriviaDatabaseApiService.fetchSessionToken()
                sessionTokenString = sessionToken.token
                await self.__openTriviaDatabaseSessionTokenRepository.update(
                    sessionToken = sessionTokenString,
                    twitchChannelId = twitchChannelId
                )

            try:
                return await self.__openTriviaDatabaseApiService.fetchTriviaQuestion(
                    sessionToken = sessionTokenString,
                    twitchChannelId = twitchChannelId
                )
            except GenericNetworkException as e:
                self.__timber.log('OpenTriviaDatabaseQuestionFetcher', f'Failed to fetch trivia question from Open Trivia Database ({attempt=}) ({maxAttempts=}) ({sessionTokenString=}) ({twitchChannelId=})', e, traceback.format_exc())

            attempt = attempt + 1

        self.__timber.log('OpenTriviaDatabaseQuestionFetcher', f'Failed to fetch trivia question from Open Trivia Database ({attempt=}) ({maxAttempts=}) ({sessionTokenString=}) ({twitchChannelId=})')
        raise GenericNetworkException(f'OpenTriviaDatabaseQuestionFetcher failed to fetch trivia question from Open Trivia Database ({attempt=}) ({maxAttempts=}) ({sessionTokenString=}) ({twitchChannelId=})')
