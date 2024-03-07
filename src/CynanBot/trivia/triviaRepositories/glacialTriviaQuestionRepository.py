from typing import Set

from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.questions.triviaQuestionType import TriviaQuestionType
from CynanBot.trivia.questions.triviaSource import TriviaSource
from CynanBot.trivia.triviaFetchOptions import TriviaFetchOptions
from CynanBot.trivia.triviaRepositories.absTriviaQuestionRepository import \
    AbsTriviaQuestionRepository
from CynanBot.trivia.triviaRepositories.glacialTriviaQuestionRepositoryInterface import \
    GlacialTriviaQuestionRepositoryInterface
from CynanBot.trivia.triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface


class GlacialTriviaQuestionRepository(
    AbsTriviaQuestionRepository,
    GlacialTriviaQuestionRepositoryInterface
):

    def __init__(
        self,
        timber: TimberInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface
    ):
        super().__init__(triviaSettingsRepository)

        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: TimberInterface = timber

    async def fetchTriviaQuestion(self, fetchOptions: TriviaFetchOptions) -> AbsTriviaQuestion:
        if not isinstance(fetchOptions, TriviaFetchOptions):
            raise TypeError(f'fetchOptions argument is malformed: \"{fetchOptions}\"')

        # TODO
        raise RuntimeError('not yet implemented')

    async def getSupportedTriviaTypes(self) -> Set[TriviaQuestionType]:
        return {
            TriviaQuestionType.MULTIPLE_CHOICE,
            TriviaQuestionType.QUESTION_ANSWER,
            TriviaQuestionType.TRUE_FALSE
        }

    async def getTriviaSource(self) -> TriviaSource:
        return TriviaSource.GLACIAL

    async def hasQuestionSetAvailable(self) -> bool:
        # TODO
        return False

    async def store(self, question: AbsTriviaQuestion) -> bool:
        if not isinstance(question, AbsTriviaQuestion):
            raise TypeError(f'question argument is malformed: \"{question}\"')

        if not await self._triviaSettingsRepository.isScraperEnabled():
            return False

        # TODO
        return False
