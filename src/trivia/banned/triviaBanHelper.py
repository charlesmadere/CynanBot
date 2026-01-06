from typing import Final

from .banTriviaQuestionResult import BanTriviaQuestionResult
from .bannedTriviaIdsRepositoryInterface import BannedTriviaIdsRepositoryInterface
from .triviaBanHelperInterface import TriviaBanHelperInterface
from ..questions.triviaSource import TriviaSource
from ..settings.triviaSettingsRepositoryInterface import TriviaSettingsRepositoryInterface
from ..triviaRepositories.glacialTriviaQuestionRepositoryInterface import GlacialTriviaQuestionRepositoryInterface
from ...funtoon.funtoonHelperInterface import FuntoonHelperInterface
from ...misc import utils as utils


class TriviaBanHelper(TriviaBanHelperInterface):

    def __init__(
        self,
        bannedTriviaIdsRepository: BannedTriviaIdsRepositoryInterface,
        funtoonHelper: FuntoonHelperInterface,
        glacialTriviaQuestionRepository: GlacialTriviaQuestionRepositoryInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface,
    ):
        if not isinstance(bannedTriviaIdsRepository, BannedTriviaIdsRepositoryInterface):
            raise TypeError(f'bannedTriviaIdsRepository argument is malformed: \"{bannedTriviaIdsRepository}\"')
        elif not isinstance(funtoonHelper, FuntoonHelperInterface):
            raise TypeError(f'funtoonHelper argument is malformed: \"{funtoonHelper}\"')
        elif not isinstance(glacialTriviaQuestionRepository, GlacialTriviaQuestionRepositoryInterface):
            raise TypeError(f'glacialTriviaQuestionRepository argument is malformed: \"{glacialTriviaQuestionRepository}\"')
        elif not isinstance(triviaSettingsRepository, TriviaSettingsRepositoryInterface):
            raise TypeError(f'triviaSettingsRepository argument is malformed: \"{triviaSettingsRepository}\"')

        self.__bannedTriviaIdsRepository: Final[BannedTriviaIdsRepositoryInterface] = bannedTriviaIdsRepository
        self.__funtoonHelper: Final[FuntoonHelperInterface] = funtoonHelper
        self.__glacialTriviaQuestionRepository: Final[GlacialTriviaQuestionRepositoryInterface] = glacialTriviaQuestionRepository
        self.__triviaSettingsRepository: Final[TriviaSettingsRepositoryInterface] = triviaSettingsRepository

    async def ban(
        self,
        triviaId: str,
        userId: str,
        triviaSource: TriviaSource,
    ) -> BanTriviaQuestionResult:
        if not utils.isValidStr(triviaId):
            raise TypeError(f'triviaId argument is malformed: \"{triviaId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not isinstance(triviaSource, TriviaSource):
            raise TypeError(f'triviaSource argument is malformed: \"{triviaSource}\"')

        await self.__glacialTriviaQuestionRepository.remove(
            triviaId = triviaId,
            originalTriviaSource = triviaSource,
        )

        if triviaSource is TriviaSource.FUNTOON:
            await self.__funtoonHelper.banTriviaQuestion(triviaId)
            return BanTriviaQuestionResult.BANNED
        else:
            return await self.__bannedTriviaIdsRepository.ban(
                triviaId = triviaId,
                userId = userId,
                triviaSource = triviaSource,
            )

    async def isBanned(
        self,
        triviaId: str,
        triviaSource: TriviaSource,
    ) -> bool:
        if not utils.isValidStr(triviaId):
            raise TypeError(f'triviaId argument is malformed: \"{triviaId}\"')
        elif not isinstance(triviaSource, TriviaSource):
            raise TypeError(f'triviaSource argument is malformed: \"{triviaSource}\"')

        if not await self.__triviaSettingsRepository.isBanListEnabled():
            return False

        return await self.__bannedTriviaIdsRepository.isBanned(
            triviaId = triviaId,
            triviaSource = triviaSource,
        )

    async def unban(
        self,
        triviaId: str,
        triviaSource: TriviaSource,
    ) -> BanTriviaQuestionResult:
        if not utils.isValidStr(triviaId):
            raise TypeError(f'triviaId argument is malformed: \"{triviaId}\"')
        elif not isinstance(triviaSource, TriviaSource):
            raise TypeError(f'triviaSource argument is malformed: \"{triviaSource}\"')

        return await self.__bannedTriviaIdsRepository.unban(
            triviaId = triviaId,
            triviaSource = triviaSource,
        )
