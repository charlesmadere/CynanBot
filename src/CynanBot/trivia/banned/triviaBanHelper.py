import CynanBot.misc.utils as utils
from CynanBot.funtoon.funtoonRepositoryInterface import \
    FuntoonRepositoryInterface
from CynanBot.trivia.banned.bannedTriviaIdsRepositoryInterface import \
    BannedTriviaIdsRepositoryInterface
from CynanBot.trivia.banned.banTriviaQuestionResult import \
    BanTriviaQuestionResult
from CynanBot.trivia.banned.triviaBanHelperInterface import \
    TriviaBanHelperInterface
from CynanBot.trivia.questions.triviaSource import TriviaSource
from CynanBot.trivia.triviaRepositories.glacialTriviaQuestionRepositoryInterface import \
    GlacialTriviaQuestionRepositoryInterface
from CynanBot.trivia.triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface


class TriviaBanHelper(TriviaBanHelperInterface):

    def __init__(
        self,
        bannedTriviaIdsRepository: BannedTriviaIdsRepositoryInterface,
        funtoonRepository: FuntoonRepositoryInterface,
        glacialTriviaQuestionRepository: GlacialTriviaQuestionRepositoryInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface
    ):
        if not isinstance(bannedTriviaIdsRepository, BannedTriviaIdsRepositoryInterface):
            raise TypeError(f'bannedTriviaIdsRepository argument is malformed: \"{bannedTriviaIdsRepository}\"')
        elif not isinstance(funtoonRepository, FuntoonRepositoryInterface):
            raise TypeError(f'funtoonRepository argument is malformed: \"{funtoonRepository}\"')
        elif not isinstance(glacialTriviaQuestionRepository, GlacialTriviaQuestionRepositoryInterface):
            raise TypeError(f'glacialTriviaQuestionRepository argument is malformed: \"{glacialTriviaQuestionRepository}\"')
        elif not isinstance(triviaSettingsRepository, TriviaSettingsRepositoryInterface):
            raise TypeError(f'triviaSettingsRepository argument is malformed: \"{triviaSettingsRepository}\"')

        self.__bannedTriviaIdsRepository: BannedTriviaIdsRepositoryInterface = bannedTriviaIdsRepository
        self.__funtoonRepository: FuntoonRepositoryInterface = funtoonRepository
        self.__glacialTriviaQuestionRepository: GlacialTriviaQuestionRepositoryInterface = glacialTriviaQuestionRepository
        self.__triviaSettingsRepository: TriviaSettingsRepositoryInterface = triviaSettingsRepository

    async def ban(
        self,
        triviaId: str,
        userId: str,
        triviaSource: TriviaSource
    ) -> BanTriviaQuestionResult:
        if not utils.isValidStr(triviaId):
            raise TypeError(f'triviaId argument is malformed: \"{triviaId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not isinstance(triviaSource, TriviaSource):
            raise TypeError(f'triviaSource argument is malformed: \"{triviaSource}\"')

        await self.__glacialTriviaQuestionRepository.remove(
            triviaId = triviaId,
            originalTriviaSource = triviaSource
        )

        if triviaSource is TriviaSource.FUNTOON:
            await self.__funtoonRepository.banTriviaQuestion(triviaId)
            return BanTriviaQuestionResult.BANNED
        else:
            return await self.__bannedTriviaIdsRepository.ban(
                triviaId = triviaId,
                userId = userId,
                triviaSource = triviaSource
            )

    async def isBanned(self, triviaId: str, triviaSource: TriviaSource) -> bool:
        if not utils.isValidStr(triviaId):
            raise TypeError(f'triviaId argument is malformed: \"{triviaId}\"')
        elif not isinstance(triviaSource, TriviaSource):
            raise TypeError(f'triviaSource argument is malformed: \"{triviaSource}\"')

        if not await self.__triviaSettingsRepository.isBanListEnabled():
            return False

        return await self.__bannedTriviaIdsRepository.isBanned(
            triviaId = triviaId,
            triviaSource = triviaSource
        )

    async def unban(
        self,
        triviaId: str,
        triviaSource: TriviaSource
    ) -> BanTriviaQuestionResult:
        if not utils.isValidStr(triviaId):
            raise TypeError(f'triviaId argument is malformed: \"{triviaId}\"')
        elif not isinstance(triviaSource, TriviaSource):
            raise TypeError(f'triviaSource argument is malformed: \"{triviaSource}\"')

        return await self.__bannedTriviaIdsRepository.unban(
            triviaId = triviaId,
            triviaSource = triviaSource
        )
