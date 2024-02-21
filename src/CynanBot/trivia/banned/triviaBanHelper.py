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
from CynanBot.trivia.triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface


class TriviaBanHelper(TriviaBanHelperInterface):

    def __init__(
        self,
        bannedTriviaIdsRepository: BannedTriviaIdsRepositoryInterface,
        funtoonRepository: FuntoonRepositoryInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface
    ):
        assert isinstance(bannedTriviaIdsRepository, BannedTriviaIdsRepositoryInterface), f"malformed {bannedTriviaIdsRepository=}"
        assert isinstance(funtoonRepository, FuntoonRepositoryInterface), f"malformed {funtoonRepository=}"
        assert isinstance(triviaSettingsRepository, TriviaSettingsRepositoryInterface), f"malformed {triviaSettingsRepository=}"

        self.__bannedTriviaIdsRepository: BannedTriviaIdsRepositoryInterface = bannedTriviaIdsRepository
        self.__funtoonRepository: FuntoonRepositoryInterface = funtoonRepository
        self.__triviaSettingsRepository: TriviaSettingsRepositoryInterface = triviaSettingsRepository

    async def ban(
        self,
        triviaId: str,
        userId: str,
        triviaSource: TriviaSource
    ) -> BanTriviaQuestionResult:
        if not utils.isValidStr(triviaId):
            raise ValueError(f'triviaId argument is malformed: \"{triviaId}\"')
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        assert isinstance(triviaSource, TriviaSource), f"malformed {triviaSource=}"

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
            raise ValueError(f'triviaId argument is malformed: \"{triviaId}\"')
        assert isinstance(triviaSource, TriviaSource), f"malformed {triviaSource=}"

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
            raise ValueError(f'triviaId argument is malformed: \"{triviaId}\"')
        assert isinstance(triviaSource, TriviaSource), f"malformed {triviaSource=}"

        return await self.__bannedTriviaIdsRepository.unban(
            triviaId = triviaId,
            triviaSource = triviaSource
        )
